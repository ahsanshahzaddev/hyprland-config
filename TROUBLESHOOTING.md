# Troubleshooting

## Symptom

Three-monitor Hyprland desktop becomes **stuttery / laggy**. Cursor and animations feel uneven. Adding a high-resolution external display (1440p) made this much more noticeable.

## Important diagnostic split

| Test | Result (this incident) |
|---|---|
| Hyprland alone (Quickshell killed) | Smooth |
| Hyprland + Quickshell | Stutter returns |
| Conclusion | Not “the monitor is broken”; shell rendering / damage is the problem |

Do **not** assume the 1440p panel itself is defective. Extra pixels increased compositor + shell workload and **exposed** a Quickshell scene-graph failure.

## Diagnostic command (Intel)

```bash
sudo intel_gpu_top
```

Watch **Render/3D**, **RC6**, and GPU frequency.

### Bad state (observed)

```text
Render/3D ≈ 98%
RC6      ≈ 0%
GPU      ≈ ~1 GHz (stuck high)
```

Killing Quickshell immediately restored normal GPU behavior.

### Healthy state (observed after fix, normal desktop apps)

Approximate ranges — **exact numbers vary with workload**:

```text
Render/3D ≈ 24–28%
RC6      ≈ 43–58%
GPU      ≈ 100–330 MHz
```

A healthy idle-ish session should **not** look like the bad state above.

## Related log signature

Quickshell / Qt Quick may log:

```text
QSGRhiLayer: Unsupported size requested
Maximum texture size: 16384
```

That means some QML layer exceeded the GPU max texture dimension (Intel Mesa often **16384**). On this system it came from an enormous expanded notification group (~27 615 px tall) backed by unbounded persisted notification history (~1602 items; one group ~838).

## Fixes already in this repository

See [docs/quickshell-gpu-fix.md](docs/quickshell-gpu-fix.md):

1. `historyLimit: 200` + trim on load/arrive  
2. Expanded group height cap ~480 px + scroll (`NotificationGroup.qml`, `WNotificationGroup.qml`)  
3. `constantlyRotate: false` on cookie clock  

## Other useful checks

```bash
# Confirm Quickshell is running
pgrep -a qs

# Hyprland version / monitors
hyprctl version
hyprctl monitors

# Quickshell logs (path may vary)
journalctl --user -b | rg -i 'quickshell|QSGRhiLayer|texture'
```

## Optional services that can add load

- `hypr-mouse-workspace.service` (evdev mouse daemon) — disable if unused  
- `elephant.service` — launcher helper; optional  

Neither was the root cause of the 98% GPU peg; Quickshell notifications + continuous animation were.
