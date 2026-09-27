# Display setup

## Capture-host layout (2026-09-27)

Logical left → right:

```text
eDP-1                HDMI-A-1 (Samsung LS27A600U)     DP-1
1920×1080 @ 60.01    2560×1440 @ 74.97                 1920×1080 @ 60.00
transform 0          transform 0                      transform 3 (rotated)
pos 0x0              pos 1920x0                       pos 4480x0
```

Files:

- `hypr/monitors.conf` — classic Hyprland monitor lines (nwg-displays)
- `hypr/monitors.lua` — Lua equivalent included by the Lua Hyprland entry

## Regenerating on a new machine

1. Start Hyprland with a minimal monitor config if needed.
2. Run `nwg-displays` (or edit monitors manually).
3. Replace `monitors.conf` / `monitors.lua` in the repo or in `~/.config/hypr/`.
4. Confirm with `hyprctl monitors`.

## Notes

- Connector names (`eDP-1`, `HDMI-A-1`, `DP-1`) are **not portable**.
- Refresh rates depend on cable/GPU/EDID; 1440p@~75 worked on the capture host over HDMI.
- Adding a high-res panel can expose shell bugs (see [quickshell-gpu-fix.md](quickshell-gpu-fix.md)); verify GPU idle with `intel_gpu_top` after display changes.
