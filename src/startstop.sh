#!/bin/sh

if pkill -f n9-button-monitor\.py; then
    echo "killed"
    cat /opt/adv-button-monitor/off.desktop >/usr/share/applications/adv-button-monitor.desktop
else
    echo "starting"
    cat /opt/adv-button-monitor/on.desktop >/usr/share/applications/adv-button-monitor.desktop
    /opt/adv-button-monitor/n9-button-monitor.py
fi
