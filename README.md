# Ambient Light ESP32

Sixty LEDs behind my monitor that mirror whatever's on my screen in real time — bright scenes glow bright, dark scenes stay dark, and colors bleed smoothly from one frame to the next instead of snapping.

## The idea

I wanted the desk-ambilight effect I'd seen in build videos, but I didn't want to buy a pre-made kit — I wanted to actually understand every layer of it: how a strip of LEDs gets addressed, how a screen becomes 60 numbers, how those numbers get from a laptop to a physical chip fast enough to feel instant. This is my **first real electronics project.** Everything here — flashing a microcontroller for the first time, wiring a strip of individually addressable LEDs, learning why gamma correction exists, chasing down a serial "device busy" error at 1am — was new to me a few weeks ago.

The pipeline, in one sentence: a Python script on my PC grabs the screen, shrinks it to one pixel per LED, corrects the color so darks don't disappear and brights don't blow out, smooths each frame toward the next so it doesn't flicker, and streams the result over serial to an ESP32, which paints it straight onto the strip.

## Why this repo looks the way it does

I'm documenting this properly — not because it's expected, but because I know six-months-from-now me will have forgotten exactly how I wired it, and because I want this to be something a stranger could actually pick up and run, not just skim. See `docs/` for the how; the code in `esp32/` and `pc/` is the what.

## What it does

- Real-time screen-to-LED color sync
- Smooth, non-flickery transitions between frames
- Dark scenes stay visibly dark instead of crushing to black
- Runs on a stripped USB phone charger as the LED power source — no dedicated PSU bought

## Quick start

See [`docs/SETUP.md`](docs/SETUP.md) for the full walkthrough, and [`docs/HARDWARE.md`](docs/HARDWARE.md) for wiring and parts.

## What's next

Currently wired over USB serial — a Wi-Fi/UDP version is planned so the ESP32 can run untethered from the laptop entirely.

