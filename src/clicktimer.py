#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide.QtGui import QWidget
from PySide.QtCore import QBasicTimer

import os
import ctypes

STATE_ON = 2
STATE_OFF = 0

BUTTON_VOLUME_UP = 2
BUTTON_VOLUME_DOWN = 3
BUTTON_POWER = 20

def getClickTypes():
  return ["singleClick","doubleClick","trebleClick",
          "longClickStart","longClickStop"]

def getButtons():
  return { "volumeUp": BUTTON_VOLUME_UP
         , "volumeDown": BUTTON_VOLUME_DOWN}

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
    self.presses = []
    self.releases = []
    self.keyPressed = False
    self.longClickStarted = False
    self.config = config
    keyActions = filter(lambda a: a.key == self.key, self.config.actionMaps)
    self.actionsByClickType = dict()
    for clickType in getClickTypes():
      acts = filter(lambda a: a.clickType == clickType, keyActions)
      self.actionsByClickType[clickType] = acts
  def nowMs(self):
    return monotonic_time() * 1000
  def receivePress(self):
    self.presses.append(self.nowMs())
    self.checkEvent()
  def receiveRelease(self):
    self.releases.append(self.nowMs())
    self.checkEvent()
  def checkEvent(self):
    now = self.nowMs()
    self.timer.stop()
    if len(self.presses) == 0:
      self.reset()
      return
    elif len(self.presses) == 1:
      press = self.presses[0]
      if len(self.releases) == 0:
        if now - press > self.config.longClickDelayMs:
          self.longClickStarted = True
          self.longClickStart()
        else:
          self.schedule(self.config.longClickDelayMs - (now - press))
          return
      elif len(self.releases) == 1:
        if self.longClickStarted:
          self.longClickStop()
        elif now - press > self.config.doubleClickDelayMs:
          self.singleClick()
        else:
          self.schedule(self.config.doubleClickDelayMs - (now - press))
      else:
        self.singleClick()
    elif len(self.presses) == 2:
      press = self.presses[0]
      if now - press > self.config.trebleClickDelayMs:
        self.doubleClick()
      else:
        self.schedule(self.config.trebleClickDelayMs - (now - press))
    elif len(self.presses) >= 3:
      self.trebleClick()
    self.releases
  def schedule(self, time):
    self.timer.start(time, self)
  def reset(self):
    self.timer.stop()
    self.presses = []
    self.releases = []
    self.longClickStarted = False
  def singleClick(self):
    self.reset()
    print str(self.key) + ": single"
    self.performActions("singleClick")
  def doubleClick(self):
    self.reset()
    print str(self.key) + ": double"
    self.performActions("doubleClick")
  def trebleClick(self):
    self.reset()
    print str(self.key) + ": treble"
    self.performActions("trebleClick")
  def longClickStart(self):
    print str(self.key) + ": long-start"
    self.performActions("longClickStart")
  def longClickStop(self):
    self.reset()
    print str(self.key) + ": long-stop"
    self.performActions("longClickStop")
  def performActions(self, clickType):
    for a in self.actionsByClickType[clickType]:
      if a.condLambda == None or a.condLambda():
        a.actionLambda()
  def timerEvent(self, e):
    self.timer.stop()
    self.checkEvent()
  def keyEvent(self, state):
    if state == STATE_ON and not self.keyPressed:
      self.keyPressed = True
      self.receivePress()
    elif state == STATE_OFF:
      self.keyPressed = False
      self.receiveRelease()

