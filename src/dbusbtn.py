#!/usr/bin/python
#N9 Button Monitor
#Copyright (C) 2013 Elliot Wolk
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import signal
import sys
import threading
import time
from traceback import print_exc

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from PySide.QtCore import QCoreApplication

signal.signal(signal.SIGINT, signal.SIG_DFL)

class DbusButton():
  def __init__(self):
    self.service = "org.freedesktop.Hal"
    self.path = "/org/freedesktop/Hal/devices/computer_logicaldev_input_0"
    self.interface = "org.freedesktop.Hal.Device"
    self.member = "Condition"
    self.delayedHandlerTimer = None
    self.patternDelayMs = 1500
    self.pattern = []
    self.handler = self.defaultHandler
  def ensureTimer(self):
    if self.delayedHandlerTimer != None:
      self.delayedHandlerTimer.cancel()
    delayS = self.patternDelayMs / 1000.0
    self.delayedHandlerTimer = threading.Timer(delayS, self.delayedHandler)
  def defaultHandler(self, button):
    print >> sys.stderr, "button: " + button
  def setHandler(self, handler):
    self.handler = handler
  def setRepeatBufferMs(self, repeatBufferMs):
    self.repeatBufferMs = repeatBufferMs
  def buttonClicked(self, btn):
    self.ensureTimer()
    self.pattern.append(btn)
    self.delayedHandlerTimer.start()
  def delayedHandler(self):
    btn = ",".join(self.pattern)
    self.pattern = []
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
