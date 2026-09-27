# Reproducibility checklist

Use after cloning this repo onto a new Arch + Hyprland install.

## What needs to be installed?

- [ ] Hyprland + xdg-desktop-portal-hyprland + PipeWire stack
- [ ] Illogical Impulse / Quickshell (`qs`) and fonts/icons deps ([PACKAGES.md](../PACKAGES.md))
- [ ] hypridle, hyprlock, hyprpaper (as used by this config)
- [ ] Optional: `nwg-displays`, `intel-gpu-tools`, `python-evdev` (mouse script)

## What configs need to be copied?

- [ ] `hypr/` → `~/.config/hypr/`
- [ ] `quickshell/ii/` → `~/.config/quickshell/ii/`
- [ ] `illogical-impulse/` → `~/.config/illogical-impulse/` (especially `config.json`)

## What scripts need to exist?

- [ ] Optional: `~/.local/bin/hypr-mouse-workspace` (and related) from `scripts/local-bin/`
- [ ] Scripts executable (`chmod +x`)

## What services need to run?

- [ ] Hyprland session itself
- [ ] Quickshell via II execs (`qs -c ii`)
- [ ] hypridle (if enabled in execs)
- [ ] Optional user units: mouse workspace / elephant — only if you use them

## What hardware assumptions exist?

- [ ] Intel iGPU path documented in [HARDWARE.md](../HARDWARE.md) (other GPUs: skip `intel_gpu_top`, use vendor tools)
- [ ] Triple-monitor layout is an example only

## What settings are machine-specific?

- [ ] `monitors.conf` / `monitors.lua`
- [ ] Wallpaper path and screen-record path in `config.json`
- [ ] Absolute paths in systemd user units
- [ ] Optional fish auto-start and chrome flags in `extras/`

## GPU / Quickshell fix present?

- [ ] `Notifications.qml` has `historyLimit: 200` (+ trim behavior)
- [ ] `NotificationGroup.qml` and `WNotificationGroup.qml` bound expanded height (~480) with scroll
- [ ] Cookie `constantlyRotate` is `false` in `config.json` (and Config defaults)

## How do I verify the installation?

- [ ] `hyprctl monitors` shows expected outputs
- [ ] Shell UI appears (bar / panels)
- [ ] Open notification center; expand groups; UI scrolls instead of freezing GPU
- [ ] No flood of `QSGRhiLayer: Unsupported size requested` / `16384` in logs

## How do I verify the GPU is behaving normally?

```bash
sudo intel_gpu_top
```

Healthy idle-ish / light desktop use should **not** resemble the old failure:

```text
~98% Render/3D
0% RC6
~1 GHz GPU
```

Expect intermittent RC6 and clocks that can drop well below 1 GHz when idle (exact numbers vary).

## How do I verify Quickshell is not causing excessive rendering?

1. Note `intel_gpu_top` with Quickshell running.
2. Stop Quickshell (`pkill qs` or II quit).
3. If Render/3D collapses and RC6 returns only when QS is dead, QS is still the problem — re-check the three GPU fixes and notification cache size.
4. Do **not** migrate old `notifications.json` with thousands of entries; let a fresh limited history rebuild.
