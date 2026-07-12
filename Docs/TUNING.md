# Tuning

All of these knobs live at the top of `pc/sender.py`. Change one at a time, save, restart the script, and watch it for a bit before changing another — they interact, and it's hard to tell what's doing what if you move several at once.

## `BRIGHTNESS_MAX` (default: `0.5`)
A hard cap on overall output brightness, applied before anything reaches the strip.
- **Too dim overall** → raise toward `0.6`–`0.7`
- **Too bright / harsh** → lower toward `0.3`–`0.4`

## `GAMMA` (default: `2.2`)
Screens and LEDs don't perceive brightness linearly — gamma correction bends the brightness curve so mid-tones look natural instead of washed out. Higher gamma pushes more of the range toward darker values.
- **Dark scenes look dead / no visible color** → lower toward `1.8`–`2.0`
- **Everything looks washed out / too bright in dark scenes** → raise toward `2.4`–`2.6`

## `BLACK_FLOOR` (default: `6`)
A minimum brightness per color channel, so genuinely dark scenes still show a faint glow instead of going completely off. This exists specifically because gamma correction alone tends to crush near-black colors to nothing.
- **Dark scenes are still totally black** → raise toward `10`–`15`
- **Blacks never look properly "off"** → lower toward `2`–`3`, or `0` to disable entirely

## `SMOOTHING` (default: `0.3`)
Controls how much each frame moves toward its target color versus staying at the previous color. This is what makes transitions gradual instead of an instant snap — every frame, the displayed color eases a fraction of the way toward the new target rather than jumping straight to it.
- **Feels laggy / slow to react to scene changes** → raise toward `0.4`–`0.5`
- **Flickery / jumpy, especially on fast-changing content** → lower toward `0.15`–`0.2`

## `FRAME_DELAY` (default: `0.02`, ~50fps)
Time between captured frames. Lower = more frequent updates, but more CPU load and more serial traffic.
- **Choppy / stuttery on a slower machine** → raise toward `0.04` (~25fps)
- **Want maximum responsiveness and your PC can handle it** → lower toward `0.015`

## Suggested starting point if defaults feel off

Most "why does this look wrong" cases come down to one of two things:
1. **Colors feel muddy or dark scenes feel dead** → it's `GAMMA` and `BLACK_FLOOR` fighting each other. Start by adjusting `BLACK_FLOOR` first, since it's the more direct fix for "darks look dead."
2. **Motion feels off** (either laggy or flickery) → it's purely `SMOOTHING`. Nudge it in small steps (`0.05` at a time) — this one is sensitive.
