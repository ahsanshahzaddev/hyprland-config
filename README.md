# Hyprland Desktop Configuration

Personal **Hyprland + Quickshell / Illogical Impulse** configuration captured from a working Arch Linux desktop (2026-09-27).

This repository is meant to be cloned after a fresh Arch + Hyprland install so the desktop can be reconstructed with the same structure and the Quickshell GPU fixes already applied.

## Components

| Component | Role |
|---|---|
| **Hyprland 0.56.x** | Compositor (Lua-based Illogical Impulse layout under `hypr/`) |
| **Quickshell (`qs`)** | Desktop shell UI (`quickshell/ii/`) |
| **Illogical Impulse** | Dotfiles / theming stack; user options in `illogical-impulse/config.json` |
| **hypridle / hyprlock / hyprpaper** | Idle, lock, wallpaper helpers |
| **Optional scripts** | Mouse workspace daemon, Alt-Tab helper (`scripts/local-bin/`) |

## Hardware (summary)

- Intel Alder Lake-P / Iris Xe (`i915`)
- Triple display: laptop 1080p@60 + Samsung 1440p@~75 + rotated external 1080p@60

See [HARDWARE.md](HARDWARE.md). Monitor layout is **machine-specific**.

## Installation

See [INSTALL.md](INSTALL.md).

## Verification / troubleshooting

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — stutter / GPU diagnosis
- [docs/quickshell-gpu-fix.md](docs/quickshell-gpu-fix.md) — root cause of the 2026-09-27 GPU peg
- [docs/reproducibility.md](docs/reproducibility.md) — checklist after install

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Packages

See [PACKAGES.md](PACKAGES.md).

## Layout

```text
hypr/                 → ~/.config/hypr/
quickshell/ii/        → ~/.config/quickshell/ii/
illogical-impulse/    → ~/.config/illogical-impulse/
scripts/local-bin/    → ~/.local/bin/
systemd/user/         → ~/.config/systemd/user/ (optional services)
extras/               → optional fish / fontconfig / chrome flags
docs/                 → design notes and incident writeups
```

## Important

- Do **not** commit `~/.cache/quickshell/` or notification history.
- Wallpaper paths and monitor connectors in this tree are from one machine; adjust on another.
- AI provider API keys are **not** stored in this repo (Illogical Impulse uses keyring / external key IDs).
