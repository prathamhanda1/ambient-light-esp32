# Setup

Follow this in order — ESP32 first, then PC. Don't connect the stripped charger's power until the wiring section says to.

## 1. Flash the ESP32 (using Thonny)

1. Download and install **Thonny** — a beginner-friendly Python IDE that can talk to MicroPython boards directly: https://thonny.org
2. Plug the ESP32 into your laptop via USB.
3. Open Thonny. In the bottom-right corner, click the interpreter selector and choose **MicroPython (ESP32)**, then select the correct COM port (Thonny usually detects this automatically).
   - If MicroPython isn't installed on the board yet, Thonny has a built-in installer under **Run → Configure interpreter → Install or update firmware**.
4. Open `esp32/main.py` from this repo and load it into Thonny (File → Open).
5. Click the **Run** (green play) button. You should see the LED strip briefly go dark (that's the startup blackout in the code) and then sit waiting.
6. Once you're confident it's working correctly, save it onto the board itself as `main.py` (**File → Save As → MicroPython device**), so it runs automatically every time the board powers on — you won't need Thonny open after that.

**Note:** the code disables Ctrl+C over serial (needed so incoming color data isn't mistaken for a keyboard interrupt). If you ever need to stop it and get back into Thonny, unplug the ESP32 and plug it back in.

## 2. Wire the hardware

With the ESP32 unplugged from power, follow [`HARDWARE.md`](HARDWARE.md) to connect:
- ESP32 GND → LED strip GND
- ESP32 RX2 (GPIO16) → LED strip Data In
- Stripped charger (+/–) → LED strip VCC/GND, with the charger plugged into the wall via its USB-C converter

Double-check the ground connections match `HARDWARE.md` before powering anything on — this matters more than any other wiring step.

## 3. Power it on

1. Plug the stripped charger into the wall (powers the LED strip).
2. Plug the ESP32 into your laptop via USB (powers the ESP32 and carries the serial data).
3. The strip should be dark at this point — that's correct, it's waiting for frame data from the PC.

## 4. Set up the PC side

1. Install Python 3.8 or newer if you don't already have it: https://python.org
2. Open this repo folder in a terminal (or VS Code's built-in terminal).
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Open `pc/sender.py` and check the `COM_PORT` value matches your ESP32's actual port:
   - **Windows:** Device Manager → Ports (COM & LPT) → look for something like "Silicon Labs CP210x" or "USB-SERIAL CH340", note the COM number.
5. Run it:
   ```
   python pc/sender.py
   ```

## 5. Confirm it's working

The LED strip should now mirror your screen's colors in real time. Try opening a colorful video or website and watching the strip react.

If nothing lights up or it looks wrong, check [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) before assuming the hardware is broken — most first-run issues are a COM port mismatch or the ESP32 still holding onto its last state from Thonny.
