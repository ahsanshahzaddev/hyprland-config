# Quickshell GPU fix (2026-09-27)

Incident write-up for the stutter / Intel GPU peg caused by Quickshell on a triple-monitor Hyprland desktop. Fixes are already present in the files in this repository.

---

## Original symptoms

- Desktop became **stuttery** after adding a **2560×1440 Samsung** display (third output).
- **Bare Hyprland** (Quickshell not running) remained **smooth**.
- With Quickshell running, Intel GPU (via `intel_gpu_top`) showed roughly:
  - **~98% Render/3D**
  - **0% RC6**
  - **~1 GHz** GPU frequency (stuck high)
- **Killing Quickshell** immediately restored normal behavior.

The new monitor increased rendering load and made the failure obvious; it was not itself the root bug.

---

## Root cause (primary)

### 1. Unbounded notification history

Persisted notification history grew without a meaningful cap.

Observed on the broken system:

| Metric | Approx. value |
|---|---|
| Persisted notifications | **~1602** |
| Largest single group | **~838** items |
| Expanded QML layer height | **~27 615 px** |
| Intel/Mesa max texture dimension | **16 384 px** |

### 2. Scene-graph / texture failure

Expanding the huge group requested a layer larger than the GPU allows, producing:

```text
QSGRhiLayer: Unsupported size requested
Maximum texture size: 16384
```

That abnormal Qt Quick scene-graph behavior correlated with the GPU staying pegged (no RC6, high clocks).

---

## Second issue — continuous cookie animation

```json
"background.widgets.clock.cookie.constantlyRotate": true
```

Continuous rotation keeps damaging/rendering the wallpaper widget every frame. On an already stressed multi-monitor Intel laptop, this is undesirable. It was disabled as part of the same session.

---

## Fixes applied

### Fix 1 — Notification history limit

**Where:** `quickshell/ii/services/Notifications.qml`

```qml
historyLimit: 200
```

**Why:** Prevent unbounded persistence from rebuilding enormous list models and layers.

**Behavior:**

- History is **trimmed when loaded** from disk.
- History is **trimmed when new notifications arrive**.

Runtime file `notifications.json` under the Quickshell cache must **not** be committed; only the service code that enforces the limit belongs in git.

### Fix 2 — Notification group size

Expanded groups are bounded around **480 px** height with **scrolling**, instead of growing the QML item indefinitely.

**Files:**

- `quickshell/ii/modules/common/widgets/NotificationGroup.qml` — `maxExpandedHeight` (~480)
- `quickshell/ii/modules/waffle/notificationCenter/WNotificationGroup.qml` — same idea for waffle notification center

This keeps layer textures under the 16384 limit even if a group still has many items.

### Fix 3 — Cookie animation

**Where:**

- `illogical-impulse/config.json` → `constantlyRotate: false`
- Default in `quickshell/ii/modules/common/Config.qml` aligned to `false`

**Why:** Avoid continuous full-time animation damage on the desktop background widget.

---

## Verification after fix

- Texture-size errors for that failure mode stopped.
- GPU returned to intermittent RC6 and lower clocks under normal desktop use.
- Example healthy-ish ranges while using the desktop (not a hard SLA):

```text
Render/3D ≈ 24–28%
RC6      ≈ 43–58%
GPU      ≈ 100–330 MHz
```

Re-check anytime with:

```bash
sudo intel_gpu_top
```

---

## Existing configuration vs troubleshooting changes

| Category | Contents |
|---|---|
| **Existing configuration** | Full Hyprland II tree, Quickshell `ii` modules, themes, keybinds, monitors, user `config.json` options unrelated to this bug |
| **Changes during GPU troubleshooting** | `historyLimit` + trim logic; `maxExpandedHeight` / scroll in both notification group widgets; `constantlyRotate: false` |

Do not “optimize away” unrelated Hyprland decoration/animation settings when applying this fix on another machine—only ensure the three fixes above are present.
