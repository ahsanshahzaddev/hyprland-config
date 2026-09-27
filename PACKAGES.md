# Packages

Only packages that are **required or directly relevant** to reproducing this Hyprland + Illogical Impulse desktop. This is not a dump of the entire system.

Sources: AUR meta packages `illogical-impulse-*`, Hyprland stack, and tools referenced by configs/scripts.

## Core (Wayland / Hyprland)

| Package | Notes |
|---|---|
| `hyprland` | Compositor (≥ 0.56 recommended for this Lua layout) |
| `xdg-desktop-portal-hyprland` | Portal for Hyprland |
| `xdg-desktop-portal` | Base portal |
| `qt6-wayland` | Qt Wayland platform |
| `polkit-kde-agent` / polkit agent | Auth agent (II may pull one) |
| `pipewire` + `wireplumber` | Audio / screen share |
| `wl-clipboard` | Clipboard |

## UI / shell (Illogical Impulse)

Install via the Illogical Impulse installer or AUR packages such as:

| Package / meta | Role |
|---|---|
| `illogical-impulse-dotfiles` (or equivalent) | Dotfiles / `~/.config/hypr` layout |
| `illogical-impulse-quickshell-git` | Quickshell shell (`qs`) |
| `illogical-impulse-basic` / fonts / icons metas | Fonts, icon themes, dependencies |
| `quickshell` (if separate) | Quickshell binary |

Exact package names change; prefer the upstream II install script for Arch.

## Hyprland ecosystem (used by this config)

| Package | Role | Optional? |
|---|---|---|
| `hypridle` | Idle daemon | No (referenced) |
| `hyprlock` | Lock screen | No (referenced) |
| `hyprpaper` | Wallpaper | Soft |
| `hyprpicker` | Color picker | Soft |
| `hyprsunset` | Night light | Soft |
| `hyprctl` | Bundled with hyprland | No |

## Utilities referenced by keybinds / scripts

| Package | Role | Optional? |
|---|---|---|
| `kitty` | Terminal (`$terminal`) | Prefer keep |
| `dolphin` | File manager | Soft |
| `firefox` / browser of choice | `$browser` | Soft |
| `fuzzel` / app launcher II uses | Launcher | Soft |
| `grim` + `slurp` | Screenshots | Soft |
| `swappy` | Screenshot annotate | Soft |
| `cliphist` | Clipboard history | Soft |
| `brightnessctl` | Brightness | Soft |
| `playerctl` | Media | Soft |
| `pamixer` / `wpctl` | Volume | Soft |
| `nwg-displays` | Monitor GUI → writes `monitors.conf` / `monitors.lua` | Soft but useful |
| `python-evdev` | Mouse workspace script | Optional |
| `python` | Scripts | If using mouse script |
| `fish` | Shell + auto-start Hypr snippet in `extras/` | Soft |
| `uwsm` | Session manager (if you use UWSM sessions) | Soft |

## Display / GPU diagnostics

| Package | Role | Optional? |
|---|---|---|
| `intel-gpu-tools` | `intel_gpu_top` | **Recommended** for Intel |
| `mesa-utils` | `glxinfo` / `eglinfo` | Soft |

## Optional desktop extras (present on capture host, not required for core)

- `code` / VS Code / Cursor (user tooling)
- `google-chrome` / Chromium (`extras/chrome-flags.conf` is optional)
- `scrcpy` (phone as webcam bind)
- AI / translation helpers II may call (keys via keyring, not this repo)

## How this host installed II

On the capture machine, AUR packages matching `illogical-impulse-*` were installed via yay. Reinstalling from AUR + copying this repo’s configs is the intended path; do not rely on `installed_listfile` paths from the old home directory (excluded from git).
