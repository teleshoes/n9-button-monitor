#!/usr/bin/python
#N9 Button Monitor
#Copyright (C) 2012 Elliot Wolk
#Copyright (C) 2013 Lcferrum
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PySide.QtGui import QWidget
from PySide.QtCore import QBasicTimer

import os
import ctypes
import sys

STATE_ON = 2
STATE_OFF = 0

BUTTON_N950CAMKEY = 1
BUTTON_VOLUME_UP = 2
BUTTON_VOLUME_DOWN = 3
BUTTON_POWER = 20

def getClickTypes():
  return ["singleClick","doubleClick","trebleClick",
          "longClickStart","longClickStop"]

def getButtons():
  return { "volumeUp": BUTTON_VOLUME_UP
         , "volumeDown": BUTTON_VOLUME_DOWN
         , "cameraButton": BUTTON_N950CAMKEY
         , "powerButton": BUTTON_POWER
         , "dbus": "dbus"}

###############

#montonic timer so that ntp adjustments cant throw off double-click timing..
__all__ = ["monotonic_time"]
CLOCK_MONOTONIC = 1 # see <linux/time.h>
CLOCK_MONOTONIC_RAW = 4 # see <linux/time.h>
class timespec(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]
librt = ctypes.CDLL('librt.so.1', use_errno=True)
clock_gettime = librt.clock_gettime
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

def monotonic_time():
  t = timespec()
  if clock_gettime(CLOCK_MONOTONIC_RAW, ctypes.pointer(t)) != 0:
    errno_ = ctypes.get_errno()
    raise OSError(errno_, os.strerror(errno_))
  return t.tv_sec + t.tv_nsec * 1e-9

###############

class ClickTimer(QWidget):
  def __init__(self, key, config):
    super(ClickTimer, self).__init__()
    self.timer = QBasicTimer()
    self.key = key
    self.keyPressed = False
    self.config = config
    self.reset()
  def reset(self):
    self.timer.stop()
    self.presses = []
    self.releases = []
    self.longClickStarted = False
  def nowMs(self):
    return monotonic_time() * 1000
  def checkEvent(self):
    now = self.nowMs()
    self.timer.stop()
    if len(self.presses) == 0:
      if self.longClickStarted and len(self.releases) > 0:
        self.click("longClickStop")
      else:
        self.reset()
    elif len(self.presses) == 1:
      press = self.presses[0]
      if len(self.releases) == 0:
        if now - press > self.config.longClickDelayMs:
          self.click("longClickStart")
          self.longClickStarted = True
        else:
          self.schedule(self.config.longClickDelayMs - (now - press))
      else:
        if now - press > self.config.doubleClickDelayMs:
          self.click("singleClick")
        else:
          self.schedule(self.config.doubleClickDelayMs - (now - press))
    elif len(self.presses) == 2:
      press = self.presses[0]
      if now - press > self.config.trebleClickDelayMs:
        self.click("doubleClick")
      else:
        self.schedule(self.config.trebleClickDelayMs - (now - press))
    else:
      self.click("trebleClick")
  def schedule(self, time):
    self.timer.start(time, self)
  def click(self, clickType):
    self.reset()
    self.config.checkConfigFile()
    print >> sys.stderr, str(self.key) + ": " + clickType

    actionMaps = self.config.getActionMapSet()
    for a in actionMaps.getActionMapsForKey(self.key, clickType):
      a.maybeRun()
  def timerEvent(self, e):
    self.timer.stop()
    self.checkEvent()
  def receivePress(self):
    self.presses.append(self.nowMs())
    self.checkEvent()
  def receiveRelease(self):
    self.releases.append(self.nowMs())
    self.checkEvent()
  def keyEvent(self, state):
    if state == STATE_ON and not self.keyPressed:
      self.keyPressed = True
      self.receivePress()
    elif state == STATE_OFF:
      self.keyPressed = False
      self.receiveRelease()

