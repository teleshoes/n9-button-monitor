[![Flattr Button](http://api.flattr.com/button/button-static-50x60.png "Flattr This!")](https://flattr.com/thing/616727 "N9 Button Monitor")

````
N9 Button Monitor 
Copyright 2012 Elliot Wolk
#####
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
#####

Control volume up/down actions

features:
-currently shines flashlight/torch from lockscreen
-focuses/snaps pix in camera, using VOL+
-playpause/prev/next from lockscreen for harmattan music suite

installation:
1) install deps {apt-get install}
xresponse
x11-utils
python-qmsystem
python-qtmobility.multimediakit
python-qtmobility.systeminfo
python-pyside.qtgui
python-pyside.qtcore

2) copy n9-button-monitor.py to phone, e.g. to MyDocs with Sync&Connect

3) open a terminal, and execute it as root like this:
devel-su -c "develsh -c 'python /home/user/MyDocs/n9-button-monitor.py'"
```
