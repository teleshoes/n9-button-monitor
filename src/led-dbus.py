#!/usr/bin/python
#N9 LED Daemon
#Copyright 2013 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide.QtGui import *
from PySide.QtCore import *
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import dbus.service
import sys
import signal

SERVICE = 'org.teleshoes.led'

LED_DEV = (''
  + '/sys/devices/platform'
  + '/i2c_omap.2/i2c-2/2-0032/leds/lp5521:channel0'
  + '/brightness'
)

signal.signal(signal.SIGINT, signal.SIG_DFL)

name = sys.argv[0]
usage = ("Usage: " + name + "\n"
  + "  Start a dbus service that sets the LED brightness {0 to 255}"
  + "  After starting the daemon, use it like this: \n"
  + "    qdbus " + SERVICE + " / led 255 #on\n"
  + "    qdbus " + SERVICE + " / led 0   #off\n"
)

def main():
  if len(sys.argv) != 1:
    print(usage)
    return 0
  else:
    app = QApplication([])
    DBusGMainLoop(set_as_default=True)
    LedDbusService()
    app.exec_()

def setLedBrightness(brightness):
  if 0 <= brightness and brightness <= 255:
    open(LED_DEV, 'w').write(str(brightness))

class LedDbusService(dbus.service.Object):
  def __init__(self):
    dbus.service.Object.__init__(self, self.getBusName(), '/')
  def getBusName(self):
    return dbus.service.BusName(
      'org.teleshoes.led', bus=dbus.SessionBus())
  @dbus.service.method('org.teleshoes.led')
  def led(self, brightness):
    try:
      setLedBrightness(int(brightness))
    except:
      pass

if __name__ == "__main__":
  sys.exit(main())
