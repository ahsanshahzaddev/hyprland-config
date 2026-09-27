#!/usr/bin/env bash

handle() {
  if echo "$1" | grep -q "^monitorremoved>>"; then
    # Modern Hyprland 0.55+ Lua configuration syntax
    hyprctl eval 'hl.monitor({ output = "eDP-1", mode = "preferred", position = "auto", scale = 1 })'
  fi
}

socat -U - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock" | while read -r line; do
  handle "$line"
done

