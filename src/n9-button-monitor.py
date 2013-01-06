#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from config import Config
from guiconfig import GuiConfig
from actions import ActionDict
from clicktimer import ClickTimer, getButtons, getClickTypes
from dbusbtn import connectButtonDbus
from camera import Camera

from QmSystem import QmKeys
from PySide.QtGui import QApplication
from QtMobility.SystemInfo import QSystemDeviceInfo

import sys
import re
import time
import subprocess

name = sys.argv[0]
usage = ("Usage:\n"
  + "  " + name + "     start monitoring buttons\n"
  + "  " + name + " -g  launch gui for configuring\n"
  + "  " + name + " -h  show this message\n"
)

def main():
  if len(sys.argv) == 2 and sys.argv[1] == '-g':
    GuiConfig().showGui()
    return 0
  elif len(sys.argv) == 2 and sys.argv[1] == '-h':
    print usage
    return 0
  elif len(sys.argv) > 1:
    print >> sys.stderr, usage
    return 1
  else:
    startMonitor()
    return 0

def dbusBtn(config, button):
  actionMaps = config.getActionMapSet()
  for a in actionMaps.getActionMapsForDbus(button):
    if a.condLambda == None or a.condLambda():
      a.actionLambda()

def startMonitor():
  camera = Camera()
  actionDict = ActionDict(camera)
  config = Config(
    actionDict,
    getButtons().keys(),
    getClickTypes())
  camera.setConfig(config)

  config.checkConfigFile()

  app = QApplication([])
  camera.initCamera()
  keys = QmKeys()
  buttonTimers = dict()
  for b in getButtons().values():
    buttonTimers[b] = ClickTimer(b, config)
  keys.keyEvent.connect(lambda k, s:
    (k in buttonTimers and buttonTimers[k].keyEvent(s)))
  connectButtonDbus(lambda button: dbusBtn(config, button))
  app.exec_()

if __name__ == "__main__":
  sys.exit(main())

