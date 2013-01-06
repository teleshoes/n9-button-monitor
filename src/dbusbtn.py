#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import sys
import time
import signal
from traceback import print_exc
 
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from PySide.QtCore import QCoreApplication

signal.signal(signal.SIGINT, signal.SIG_DFL)
dbus_service="org.freedesktop.Hal"
dbus_path="/org/freedesktop/Hal/devices/computer_logicaldev_input_0"
dbus_interface="org.freedesktop.Hal.Device"
dbus_member="Condition"

## for some horrible reason, i get 8 clicks sometimes
## this buffer ignores repeated clicks within a certain time
## set it to -1 to never ignore
repeat_buffer_millis=800

last_button_click_millis = dict()

def button_clicked(button, handler):
  now_millis = int(round(time.time() * 1000))
  if button in last_button_click_millis:
    then_millis = last_button_click_millis[button]
    if now_millis - then_millis < repeat_buffer_millis:
      print >> sys.stderr, "  ignored: " + button
      return

  last_button_click_millis[button] = now_millis
  handler(button)

def defaultHandler(button):
  print >> sys.stderr, "button: " + button

def connectButtonDbus(handler=defaultHandler):
  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
  bus = dbus.SystemBus()
  try:
    obj = bus.get_object(dbus_service, dbus_path)
    iface = dbus.Interface(obj, dbus_interface)
  except dbus.DBusException:
    print_exc()
    sys.exit(1)
 
  iface.connect_to_signal(dbus_member,
    lambda cond, arg: button_clicked(arg, handler))

if __name__ == '__main__':
  app = QCoreApplication([])
  connectButtonDbus()
  app.exec_()
