#!/usr/bin/env python3
"""
Hyprland Attack Shark Mouse Workspace Modifier Daemon

Maps the lower extra side button (BTN_SIDE / 275) as a workspace modifier:
- Lower extra button held + Left Click  -> workspace r-1 (previous workspace)
- Lower extra button held + Right Click -> workspace r+1 (next workspace)
- Lower extra button released           -> normal LMB/RMB/motion/wheel behavior
- BTN_SIDE itself is swallowed so Chrome/Figma NEVER triggers Browser Back!

Supports connection via Bluetooth (X11mouse2), 2.4G USB Dongle (2.4G Wireless Device), or USB Cable.
"""

import sys
import os
import time
import signal
import subprocess
import logging
import fcntl
import glob
from evdev import InputDevice, UInput, ecodes, list_devices

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

# Single instance lock file to prevent duplicate processes
LOCK_FILE = "/tmp/hypr-mouse-workspace.lock"

def acquire_single_instance_lock():
    """Ensure only one instance of the daemon runs at a time."""
    try:
        lock_fd = open(LOCK_FILE, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except (IOError, OSError):
        logging.warning("Another instance of hypr-mouse-workspace is already running. Exiting.")
        sys.exit(0)

# Target modifier button: lower extra button (BTN_SIDE / 275)
MODIFIER_BUTTON = ecodes.BTN_SIDE

# Target mouse keywords and vendor IDs to match Attack Shark mouse via Bluetooth, 2.4G Dongle, or USB
TARGET_MOUSE_KEYWORDS = ['x11mouse', 'attack', 'shark', '2.4g wireless device', '2.4g']
TARGET_VENDORS = [0x1d57, 0x045e]  # 0x1d57 = 2.4G Dongle, 0x045e = Bluetooth / USB

def find_mouse_device():
    """Dynamically locate the Attack Shark physical mouse device (Bluetooth, 2.4G Dongle, or USB)."""
    target_candidates = []

    for path in list_devices():
        try:
            dev = InputDevice(path)
            name_lower = dev.name.lower()

            # Ignore virtual devices and uinput
            if any(v in name_lower for v in ['ydotool', 'uinput', 'virtual', 'hyprland', 'modifier']):
                continue

            caps = dev.capabilities()
            if ecodes.EV_KEY in caps:
                keys = caps[ecodes.EV_KEY]
                # Must have both BTN_LEFT and BTN_SIDE
                if ecodes.BTN_LEFT in keys and ecodes.BTN_SIDE in keys:
                    is_match = (
                        any(kw in name_lower for kw in TARGET_MOUSE_KEYWORDS) or
                        dev.info.vendor in TARGET_VENDORS
                    )
                    if is_match:
                        target_candidates.append(dev)
        except Exception:
            continue

    if target_candidates:
        for dev in target_candidates:
            if 'mouse' in dev.name.lower():
                return dev
        return target_candidates[0]

    return None

def create_virtual_mouse(phys_dev):
    """Create virtual uinput mouse with explicit pointer capabilities."""
    caps = {
        ecodes.EV_KEY: [
            ecodes.BTN_LEFT,
            ecodes.BTN_RIGHT,
            ecodes.BTN_MIDDLE,
            ecodes.BTN_SIDE,
            ecodes.BTN_EXTRA,
        ],
        ecodes.EV_REL: [
            ecodes.REL_X,
            ecodes.REL_Y,
            ecodes.REL_WHEEL,
            ecodes.REL_HWHEEL,
        ],
    }

    return UInput(
        events=caps,
        name="Attack Shark Pointer Modifier",
        vendor=phys_dev.info.vendor,
        product=phys_dev.info.product,
        version=phys_dev.info.version,
        bustype=phys_dev.info.bustype
    )

def get_hyprland_env():
    """Dynamically resolve HYPRLAND_INSTANCE_SIGNATURE and XDG_RUNTIME_DIR at runtime."""
    env = os.environ.copy()
    xdg_runtime = env.get('XDG_RUNTIME_DIR', f'/run/user/{os.getuid()}')
    env['XDG_RUNTIME_DIR'] = xdg_runtime

    # Scan for active Hyprland socket directory
    socket_paths = glob.glob(f'{xdg_runtime}/hypr/*/.socket.sock') + glob.glob('/tmp/hypr/*/.socket.sock')
    if socket_paths:
        sig = os.path.basename(os.path.dirname(socket_paths[0]))
        env['HYPRLAND_INSTANCE_SIGNATURE'] = sig

    return env

def switch_workspace(direction):
    """Dispatch Hyprland workspace change cleanly with dynamic environment resolution."""
    cmd = 'hl.dsp.focus({ workspace = "r-1" })' if direction == "prev" else 'hl.dsp.focus({ workspace = "r+1" })'
    env = get_hyprland_env()
    try:
        subprocess.Popen(
            ["hyprctl", "dispatch", cmd],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        logging.error(f"Failed to dispatch hyprctl workspace: {e}")

class MouseDaemon:
    def __init__(self):
        self.mouse = None
        self.ui = None
        self.running = True

    def cleanup(self):
        logging.info("Cleaning up mouse grab and uinput device...")
        if self.mouse:
            try:
                self.mouse.ungrab()
            except Exception:
                pass
            try:
                self.mouse.close()
            except Exception:
                pass
            self.mouse = None

        if self.ui:
            try:
                self.ui.close()
            except Exception:
                pass
            self.ui = None

    def run(self):
        def handle_signal(sig, frame):
            logging.info(f"Received signal {sig}, stopping daemon...")
            self.running = False

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        while self.running:
            dev = find_mouse_device()
            if not dev:
                logging.info("Waiting for Attack Shark mouse device to connect...")
                time.sleep(2)
                continue

            try:
                self.mouse = dev
                logging.info(f"Connected to mouse: {dev.name} ({dev.path})")

                self.ui = create_virtual_mouse(dev)
                self.mouse.grab()
                logging.info("Grabbed mouse input successfully.")

                for event in self.mouse.read_loop():
                    if not self.running:
                        break

                    # Hardware real-time active keys on physical mouse
                    active_keys = self.mouse.active_keys()
                    modifier_held = (MODIFIER_BUTTON in active_keys)

                    # 1. SWALLOW BTN_SIDE (Lower Side Button) ALWAYS
                    # Prevents Chrome, Figma, and browsers from triggering Browser Back
                    if event.type == ecodes.EV_KEY and event.code == MODIFIER_BUTTON:
                        continue

                    # 2. When lower side button is physically held down:
                    if modifier_held:
                        if event.type == ecodes.EV_KEY and event.code in (ecodes.BTN_LEFT, ecodes.BTN_RIGHT):
                            if event.value == 1:  # Button press down
                                if event.code == ecodes.BTN_LEFT:
                                    logging.info("Modifier + LMB -> Workspace Previous")
                                    switch_workspace("prev")
                                elif event.code == ecodes.BTN_RIGHT:
                                    logging.info("Modifier + RMB -> Workspace Next")
                                    switch_workspace("next")
                            # Swallow both press and release of LMB/RMB while modifier is held
                            continue

                    # 3. When lower side button is NOT held (normal clicks, right click, motion, wheel):
                    self.ui.write(event.type, event.code, event.value)
                    if event.type == ecodes.EV_SYN:
                        self.ui.syn()

            except (OSError, IOError) as err:
                logging.warning(f"Mouse disconnected or read error: {err}")
            except Exception as err:
                logging.error(f"Unexpected error in event loop: {err}")
            finally:
                self.cleanup()
                if self.running:
                    time.sleep(2)

        logging.info("Daemon exited cleanly.")

if __name__ == "__main__":
    lock_fd = acquire_single_instance_lock()
    daemon = MouseDaemon()
    daemon.run()
