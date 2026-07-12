"""
ESP32 Ambient Light Sync - Receiver (MicroPython)

Listens over USB serial for a 4-byte 'SYNC' header followed by
NUM_LEDS * 3 bytes of RGB color data, then writes it to the NeoPixel
strip. Pairs with the PC-side sender script (mss + Pillow + pyserial).

Hardware:
    - WS2812B LED strip, data line on GPIO 16
    - 60 LEDs

Notes:
    - micropython.kbd_intr(-1) disables Ctrl+C over serial, since the
      incoming color-data stream would otherwise risk being misread as
      a keyboard interrupt. This means Thonny's Stop button may not work
      normally while this is running - unplug/replug the board to regain
      control if you need to re-flash.
    - Save this as main.py so it auto-runs on boot once you're happy
      with it; otherwise just run it directly in Thonny for testing.
"""

import machine
import neopixel
import sys
import uselect
import micropython

micropython.kbd_intr(-1)  # disable Ctrl+C - see note above

DATA_PIN = 16
NUM_LEDS = 60

strip = neopixel.NeoPixel(machine.Pin(DATA_PIN, machine.Pin.OUT), NUM_LEDS)

# Clear any leftover state from a previous script/test before waiting for data
strip.fill((0, 0, 0))
strip.write()

usb_watcher = uselect.poll()
usb_watcher.register(sys.stdin, uselect.POLLIN)


def wait_for_sync():
    """Block until the 4-byte 'SYNC' header is seen on stdin, byte by byte."""
    sync_sequence = [b'S', b'Y', b'N', b'C']
    sync_index = 0
    while sync_index < 4:
        if usb_watcher.poll(10):
            char = sys.stdin.buffer.read(1)
            if char == sync_sequence[sync_index]:
                sync_index += 1
            elif char == b'S':
                sync_index = 1  # allow re-sync if 'S' appears mid-search
            else:
                sync_index = 0


while True:
    wait_for_sync()

    buffer = bytearray()
    while len(buffer) < NUM_LEDS * 3:
        if usb_watcher.poll(10):
            chunk = sys.stdin.buffer.read(NUM_LEDS * 3 - len(buffer))
            if chunk:
                buffer.extend(chunk)

    for i in range(NUM_LEDS):
        strip[i] = (buffer[i * 3], buffer[(i * 3) + 1], buffer[(i * 3) + 2])
    strip.write()
