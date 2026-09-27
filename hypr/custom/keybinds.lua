hl.bind("CTRL+SUPER+ALT+Slash", hl.dsp.exec_cmd("xdg-open ~/.config/hypr/custom/keybinds.lua"), {description = "Edit user keybinds"} )

-- Alt+Tab Application Switcher (Current Workspace Only)
hl.bind("ALT + Tab", hl.dsp.exec_cmd("python3 ~/.local/bin/hypr-alt-tab.py next"), { repeating = true, description = "Window: Cycle next on workspace" })
hl.bind("ALT + SHIFT + Tab", hl.dsp.exec_cmd("python3 ~/.local/bin/hypr-alt-tab.py prev"), { repeating = true, description = "Window: Cycle previous on workspace" })
