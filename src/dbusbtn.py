#!/usr/bin/python
#N9 Button Monitor
#Copyright (C) 2012 Elliot Wolk
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time
import signal
from traceback import print_exc
 
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from PySide.QtCore import QCoreApplication

signal.signal(signal.SIGINT, signal.SIG_DFL)

class DbusButton():
  def __init__(self):
    self.service="org.freedesktop.Hal"
    self.path="/org/freedesktop/Hal/devices/computer_logicaldev_input_0"
    self.interface="org.freedesktop.Hal.Device"
    self.member="Condition"

    self.repeatBufferMs = 800

    self.lastClickMs = dict()
    self.handler = self.defaultHandler
  def defaultHandler(self, button):
    print >> sys.stderr, "button: " + button
  def setHandler(self, handler):
    self.handler = handler
  def setRepeatBufferMs(self, repeatBufferMs):
    self.repeatBufferMs = repeatBufferMs
  def buttonClicked(self, btn):
    nowMs = int(round(time.time() * 1000))
    if btn in self.lastClickMs:
      if nowMs - self.lastClickMs[btn] < self.repeatBufferMs:
        print >> sys.stderr, "  ignored: " + btn
        return
    self.lastClickMs[btn] = nowMs
    self.handler(btn)
  def connectButtonDbus(self):
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    try:
      obj = bus.get_object(self.service, self.path)
      iface = dbus.Interface(obj, self.interface)
    except dbus.DBusException:
      print_exc()
      sys.exit(1)
 
    iface.connect_to_signal(self.member,
      lambda cond, arg: self.buttonClicked(arg))

if __name__ == '__main__':
  app = QCoreApplication([])
  DbusButton().connectButtonDbus()
  app.exec_()
