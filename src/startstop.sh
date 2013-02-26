#!/bin/sh
#N9 Button Monitor
#Copyright (C) 2013 Elliot Wolk, Lcferrum
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

if pkill -f n9-button-monitor\.py; then
	cat /opt/n9-button-monitor/data/off.desktop >/usr/share/applications/n9-button-monitor.desktop
else
	cat /opt/n9-button-monitor/data/on.desktop >/usr/share/applications/n9-button-monitor.desktop
	/opt/n9-button-monitor/bin/n9-button-monitor.py
fi
