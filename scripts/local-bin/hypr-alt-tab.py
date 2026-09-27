#!/usr/bin/env python3
"""
Hyprland Alt+Tab Application Switcher (Current Workspace Only)

Features:
- Restricted strictly to open windows on current active workspace
- Sorts windows by focusHistoryID (Most-Recently-Used / MRU order)
- Preserves Super+D full-width / maximized state (fullscreen == 1) across Alt+Tab cycling
"""

import sys
import json
import subprocess

def main():
    direction = sys.argv[1] if len(sys.argv) > 1 else "next"

    # Get active window info
    try:
        active_res = subprocess.run(['hyprctl', 'activewindow', '-j'], capture_output=True, text=True, check=True)
        active_win = json.loads(active_res.stdout)
    except Exception:
        active_win = {}

    active_ws_id = active_win.get('workspace', {}).get('id')

    if active_ws_id is None:
        # Fallback to activeworkspace query if no window is currently focused
        try:
            ws_res = subprocess.run(['hyprctl', 'activeworkspace', '-j'], capture_output=True, text=True, check=True)
            active_ws_id = json.loads(ws_res.stdout).get('id')
        except Exception:
            return

    if active_ws_id is None:
        return

    # Check if currently active window is in Super+D maximized mode (fullscreen == 1)
    was_maximized = (active_win.get('fullscreen') == 1)

    # Get all clients
    try:
        clients_res = subprocess.run(['hyprctl', 'clients', '-j'], capture_output=True, text=True, check=True)
        clients = json.loads(clients_res.stdout)
    except Exception:
        return

    # Filter clients strictly belonging to current active workspace
    ws_clients = [c for c in clients if c.get('workspace', {}).get('id') == active_ws_id]

    # Handle 0 or 1 windows gracefully
    if len(ws_clients) <= 1:
        return

    # Sort clients by focusHistoryID (0 = active, 1 = previously focused, etc.)
    ws_clients.sort(key=lambda c: c.get('focusHistoryID', 999))

    # Determine target window
    target_win = ws_clients[-1] if direction == "prev" else ws_clients[1]
    target_addr = target_win.get('address')
    target_fullscreen = target_win.get('fullscreen', 0)

    if not target_addr:
        return

    # 1. Dispatch focus to target window using valid Illogical Impulse Lua dispatcher syntax
    focus_cmd = f'hl.dsp.focus({{ window = "address:{target_addr}" }})'
    subprocess.run(['hyprctl', 'dispatch', focus_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Preserve Super+D full-width maximized state if previous active window was maximized (fullscreen == 1)
    if was_maximized and target_fullscreen != 1:
        maximize_cmd = 'hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle" })'
        subprocess.run(['hyprctl', 'dispatch', maximize_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    main()
