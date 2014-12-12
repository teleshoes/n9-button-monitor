#!/usr/bin/python
#N9 Button Monitor
#Copyright (C) 2013 Elliot Wolk
#Copyright (C) 2013 Lcferrum
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from config import Config
from guiconfig import GuiConfig
from actions import ActionDict
from clicktimer import ClickTimer, getButtons, getClickTypes
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

def dbusBtnClicked(config, button):
  config.checkConfigFile()
  actionMaps = config.getActionMapSet()
  for a in actionMaps.getActionMapsForKey("dbusMessage", button):
    a.maybeRun()

def prxBtnClicked(config, state):
  config.checkConfigFile()
  actionMaps = config.getActionMapSet()
  for a in actionMaps.getActionMapsForKey("proximitySensor", state):
    a.maybeRun()

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
  config.dbusButton.setHandler(
    lambda button: dbusBtnClicked(config, button))
  config.dbusButton.connectButtonDbus()
  config.proximityButton.setHandler(
    lambda state: prxBtnClicked(config, state))
  config.proximityButton.connectProximityButton()
  app.exec_()

if __name__ == "__main__":
  sys.exit(main())

