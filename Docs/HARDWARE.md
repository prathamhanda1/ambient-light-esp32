# Hardware

## Parts used

| Part | Notes |
|---|---|
| ESP32 dev board | Runs the receiver code, powered via USB from the laptop |
| WS2812B LED strip (60 LEDs) | Individually addressable, data-driven |
| USB phone charger (stripped) | Repurposed as the 5V power source for the LED strip — cut open, output wires exposed and used directly |
| USB-C to wall adapter/converter | Lets the stripped charger's cable plug into a normal wall socket |
| Male-to-female jumper wires | ESP32 → LED strip connections (ground + data) |

No dedicated LED power supply was bought — the stripped charger does that job.

## Wiring

```
LAPTOP ──USB──> ESP32  (power + serial data for the sync protocol)

ESP32 GND ───────────────┐
                         ├──> WS2812B GND
Stripped charger (–) ────┘

ESP32 RX2 (GPIO16) ──────────> WS2812B Data In

Stripped charger (+) ────────> WS2812B VCC (5V)
```

**Why the grounds matter:** the ESP32 and the stripped charger are two separate power sources, but they both connect to the LED strip's ground rail — this ties them to a shared ground reference through the strip itself. Without a common ground, the data signal from the ESP32 has no consistent reference point against the LED strip's power, and the strip can behave erratically or not light at all. This is already satisfied in the wiring above; if you ever move the charger's ground to a different point, make sure it's still tied back to the ESP32's ground somewhere.

**Why GPIO16 / RX2:** on this ESP32 board, the pin silkscreened "RX2" corresponds to GPIO16 — the same pin `DATA_PIN = 16` refers to in `esp32/main.py`. If you're using a different ESP32 board, check its pinout diagram, since silkscreen labels vary between boards.

## A note on the stripped-charger approach

This works and is a fine way to get a project running without buying dedicated hardware, but a few things worth knowing if this setup stays long-term:

- Charger output should be genuinely **5V** — check the charger's printed label before assuming. Most basic phone chargers are 5V, but fast-charging chargers can output higher voltages that would damage the LED strip.
- No capacitor or resistor is currently in the signal/power path. These are common, cheap additions (a ~1000µF capacitor across the strip's power input, and a ~330–470Ω resistor on the data line) that absorb power spikes and clean up the data signal — worth adding if you see occasional flickering or want this to be more bulletproof before enclosing it.
- All connections are currently on jumper wires, not soldered. Fine for a project still being iterated on; worth soldering once the design is final, since loose jumper wires are a common source of intermittent glitches.

## Board reference

If you're unsure of your own board's exact pin layout, search for your ESP32 board's name + "pinout" — silkscreen labels (like "RX2") and GPIO numbers don't always match intuitively across different ESP32 variants.
