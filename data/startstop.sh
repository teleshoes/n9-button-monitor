#!/bin/sh

if pkill -0 -f n9-button-monitor.py; then
  initctl stop apps/n9-button-monitor
  sed -i s/on\.png/off\.png/ /usr/share/applications/n9bm-toggle.desktop
else
  initctl start apps/n9-button-monitor
  sed -i s/off\.png/on\.png/ /usr/share/applications/n9bm-toggle.desktop
fi
