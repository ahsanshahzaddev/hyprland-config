# Changelog

Chronological record of **configuration-relevant** changes. Distinguishes pre-existing Illogical Impulse setup from GPU troubleshooting on 2026-09-27.

Dates use the troubleshooting session calendar (UTC+5 host).

---

## 2026-09-27 — Quickshell GPU / stutter fixes

### Context

After adding a Samsung LS27A600U @ 2560×1440 ~75 Hz as a third display, the Hyprland session became stuttery. Bare Hyprland was smooth; Quickshell was the culprit. Intel GPU sat near 98% Render/3D with RC6 ≈ 0%.

### Fixed

- Capped Quickshell notification history at **`historyLimit: 200`** (`Notifications.qml`).
- Trim history on load and when new notifications arrive.
- Bounded expanded notification group height to **~480 px** with scrolling:
  - `NotificationGroup.qml` (`maxExpandedHeight`)
  - `WNotificationGroup.qml` (waffle notification center)
- Disabled continuous cookie clock rotation:
  - `illogical-impulse/config.json` → `background.widgets.clock.cookie.constantlyRotate: false`
  - Default in `Config.qml` set to `false` for the same key
- Eliminated `QSGRhiLayer: Unsupported size requested` / max texture **16384** condition caused by a ~27k-px-tall notification layer.

### Verified (post-fix, same session)

- No more 16384 texture-size errors in Quickshell logs for that failure mode.
- GPU no longer stuck ~98% Render/3D with RC6 at 0%.
- Healthy idle-ish desktop measurements were roughly **Render/3D ≈ 24–28%**, **RC6 ≈ 43–58%**, **GPU ≈ 100–330 MHz** (workload-dependent).
- Triple display including 1440p@~75 Hz remained usable.

### Documentation added

- `docs/quickshell-gpu-fix.md`
- `TROUBLESHOOTING.md`
- This changelog entry

### Not changed by the GPU fix

- Hyprland monitor layout, keybinds, decorations, animations (left as the working Illogical Impulse setup).
- Live system was audited and packaged into this repo **without** further “cleanup” edits.

---

## Pre-existing (Illogical Impulse baseline)

Captured as-is from `~/.config/{hypr,quickshell/ii,illogical-impulse}` on 2026-09-27. Includes:

- Hyprland Lua entry (`hyprland.lua`) + `custom/` extras
- Classic `hyprland.conf` + includes (`keybinds.conf`, `execs.conf`, `general.conf`, …)
- `monitors.conf` / `monitors.lua` from nwg-displays (three outputs)
- Full Quickshell `ii` tree
- User `config.json` (wallpaper path, AI key *IDs* only, cookie settings, etc.)

No fabricated older changelog entries; original dirs were not under a useful git history for this purpose.
