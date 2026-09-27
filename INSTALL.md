# Installation (fresh Arch → this desktop)

Goal: after a normal Arch install and a working Wayland/Hyprland baseline, clone this repo and restore configs **without destroying** an already-good session. Prefer copy or symlink; review machine-specific files first.

## 0. Prerequisites

- Arch Linux (or compatible) with a user account and sudo
- Network access for AUR / packages
- This repository cloned, e.g.:

```bash
git clone <your-fork-or-remote-url> ~/hyprland-config
cd ~/hyprland-config
```

## 1. Required packages

Install Hyprland + Illogical Impulse stack. Preferred: **upstream Illogical Impulse installer** for Arch, which pulls Quickshell and deps.

Alternatively install packages listed in [PACKAGES.md](PACKAGES.md) via `pacman` / `yay`, including at least:

- `hyprland`, portals, PipeWire
- Illogical Impulse / Quickshell AUR packages
- `hypridle`, `hyprlock`, `hyprpaper` (as used by this config)
- Recommended: `intel-gpu-tools` (Intel GPUs)

Do **not** blindly reinstall over a working machine; this guide is for **new** installs.

## 2. Required directories

```bash
mkdir -p ~/.config ~/.local/bin ~/.config/systemd/user
```

## 3. Install configs (non-destructive pattern)

**Back up anything that already exists**, then copy (or symlink) from the repo:

```bash
REPO="$HOME/hyprland-config"

# Backup live dirs if present
for d in hypr quickshell illogical-impulse; do
  if [ -e "$HOME/.config/$d" ]; then
    mv "$HOME/.config/$d" "$HOME/.config/${d}.bak.$(date +%Y%m%d%H%M%S)"
  fi
done

# Hyprland
cp -a "$REPO/hypr" "$HOME/.config/hypr"

# Quickshell II tree
mkdir -p "$HOME/.config/quickshell"
cp -a "$REPO/quickshell/ii" "$HOME/.config/quickshell/ii"

# Illogical Impulse user config
mkdir -p "$HOME/.config/illogical-impulse"
cp -a "$REPO/illogical-impulse/." "$HOME/.config/illogical-impulse/"
```

Symlink variant (easier to keep git in sync):

```bash
ln -sfn "$REPO/hypr" ~/.config/hypr
ln -sfn "$REPO/quickshell/ii" ~/.config/quickshell/ii
# Keep config.json as a real file if you edit secrets/paths locally:
mkdir -p ~/.config/illogical-impulse
cp "$REPO/illogical-impulse/config.json" ~/.config/illogical-impulse/config.json
```

## 4. Machine-specific edits (required)

Edit after copy:

1. **`~/.config/hypr/monitors.conf`** and **`monitors.lua`** — connectors, resolutions, positions, transforms ([HARDWARE.md](HARDWARE.md)). Prefer regenerating with `nwg-displays`.
2. **`~/.config/illogical-impulse/config.json`**
   - `background.wallpaperPath` → your wallpaper file
   - `screenRecord.savePath` → your Videos/recordings dir
   - AI `key_id` entries are placeholders; configure keys via II/keyring, do not paste secrets into git
3. Confirm **`constantlyRotate`** remains **`false`** for cookie clock (GPU-friendly).

## 5. Quickshell / Illogical Impulse

- Shell config name used by this setup: **`ii`** (`qs -c ii` / II default).
- GPU fixes live in:
  - `quickshell/ii/services/Notifications.qml` (`historyLimit`)
  - `quickshell/ii/modules/common/widgets/NotificationGroup.qml`
  - `quickshell/ii/modules/waffle/notificationCenter/WNotificationGroup.qml`
  - `illogical-impulse/config.json` + `Config.qml` defaults

Ensure the Quickshell binary from II AUR/packages is on `PATH` (`qs`).

## 6. Scripts

```bash
REPO="$HOME/hyprland-config"
cp -a "$REPO/scripts/local-bin/." "$HOME/.local/bin/"
chmod +x "$HOME/.local/bin/"*
```

Optional mouse workspace daemon needs `python-evdev` and often membership in group `input`.

## 7. Permissions

```bash
# If using hypr-mouse-workspace
sudo usermod -aG input "$USER"
# re-login after group change
```

## 8. Services (optional)

Portable unit templates are under `systemd/user/`. The mouse daemon unit uses systemd’s `%h` (user home) so it is not hard-coded to one username:

```bash
cp "$REPO/systemd/user/"*.service ~/.config/systemd/user/
systemctl --user daemon-reload
# Only if you want them:
# systemctl --user enable --now hypr-mouse-workspace.service
# systemctl --user enable --now elephant.service
```

Hyprland-side startup is primarily via `hypr/execs.conf` / II execs — review after install.

## 9. Environment variables

Capture host used II defaults; optional extras:

- `extras/environment.d/` — only if you intentionally use user environment drop-ins
- Fish auto-start: `extras/fish/conf.d/auto-Hypr.fish` → `~/.config/fish/conf.d/` (optional)

No secrets belong in environment files committed to git.

## 10. Start Hyprland

From TTY or display manager, start your usual Hyprland session (UWSM, `Hyprland`, or II’s `start-hyprland` if installed).

Confirm Quickshell starts (II execs / `qs -c ii`).

## 11. Verification

1. Three (or your) monitors match [HARDWARE.md](HARDWARE.md) / your edits.
2. Shell UI loads (bar, overlays).
3. Notification center opens; large histories do not freeze the GPU.
4. GPU health (Intel):

```bash
sudo intel_gpu_top
```

Healthy idle-ish desktop should **not** show ~98% Render/3D, 0% RC6, stuck ~1 GHz.

5. Full checklist: [docs/reproducibility.md](docs/reproducibility.md).

## Safety notes

- This guide never runs destructive package reinstalls on an already-working desktop.
- Do not copy `~/.cache/quickshell/` or `notifications.json` from an old machine.
- Review `.gitignore` before committing local changes.
