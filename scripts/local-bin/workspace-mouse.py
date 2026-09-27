#!/usr/bin/env python3

import subprocess
from evdev import InputDevice, ecodes

DEVICE = "/dev/input/event25"

BTN_SIDE = ecodes.BTN_SIDE
BTN_LEFT = ecodes.BTN_LEFT
BTN_RIGHT = ecodes.BTN_RIGHT

device = InputDevice(DEVICE)

side_held = False


def workspace(direction: str):
    subprocess.run(
        ["hyprctl", "dispatch", "workspace", direction],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


print(f"Watching {device.name} ({DEVICE})")

for event in device.read_loop():

    if event.type != ecodes.EV_KEY:
        continue

    # Button press/release
    if event.code == BTN_SIDE:
        if event.value == 1:
            side_held = True
        elif event.value == 0:
            side_held = False

    elif event.value == 1 and side_held:

        if event.code == BTN_LEFT:
            workspace("r-1")

        elif event.code == BTN_RIGHT:
            workspace("r+1")
