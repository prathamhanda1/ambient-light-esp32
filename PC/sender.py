import serial
import time
from mss import mss
from PIL import Image

# ---- connection ----
COM_PORT = 'COM3'
BAUD_RATE = 115200
NUM_LEDS = 60

# ---- tuning knobs (adjust these to taste) ----
BRIGHTNESS_MAX = 0.5      # overall cap; raise for brighter, lower for dimmer
GAMMA = 1.5               # gentler gamma so dark colors survive
BLACK_FLOOR = 6           # min brightness for dark pixels (applied by overall brightness, not per-channel)
SMOOTHING = 0.3           # transition speed: lower = smoother/slower, higher = snappier (0..1)
FRAME_DELAY = 0.02        # ~50 fps target

# gamma + brightness lookup table (NO per-channel floor here - that caused
# dark colors like brown/orange to flatten toward white)
gamma_table = []
for i in range(256):
    v = int(((i / 255.0) ** GAMMA) * 255 * BRIGHTNESS_MAX)
    gamma_table.append(v)
full_table = gamma_table * 3           # apply same curve to R, G, B

esp32 = serial.Serial(COM_PORT, BAUD_RATE)
time.sleep(2)                          # let the serial connection settle

# smoothed state: what the LEDs are currently showing (float for smooth math)
current = [[0.0, 0.0, 0.0] for _ in range(NUM_LEDS)]

with mss() as sct:
    monitor = sct.monitors[1]          # monitors[1] = primary screen
    while True:
        # 1. capture screen
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # 2. shrink to one pixel per LED (NEAREST is fast)
        tiny = img.resize((NUM_LEDS, 1), Image.Resampling.NEAREST)

        # 3. gamma + brightness
        corrected = tiny.point(full_table)
        target_pixels = list(corrected.getdata())   # list of (r,g,b) targets

        # 4. ease current colors toward targets, floor by brightness, pack for strip
        out = bytearray()
        for i in range(NUM_LEDS):
            tr, tg, tb = target_pixels[i]
            current[i][0] += (tr - current[i][0]) * SMOOTHING
            current[i][1] += (tg - current[i][1]) * SMOOTHING
            current[i][2] += (tb - current[i][2]) * SMOOTHING
            r = int(current[i][0]); g = int(current[i][1]); b = int(current[i][2])

            # lift dark pixels while preserving color ratio (keeps brown/orange from washing to white)
            peak = max(r, g, b)
            if 0 < peak < BLACK_FLOOR:
                scale = BLACK_FLOOR / peak
                r = int(r * scale); g = int(g * scale); b = int(b * scale)

            out += bytes((r, g, b))    # plain RGB; ESP32's neopixel library handles GRB internally

        # 5. send with SYNC header
        esp32.write(b'SYNC' + out)
        time.sleep(FRAME_DELAY)