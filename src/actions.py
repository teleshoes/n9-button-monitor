#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from QtMobility.SystemInfo import QSystemDeviceInfo
from PySide import QtGui

import sys
import subprocess
import time

SCREENSHOT_DIR = '/home/user/MyDocs'

MUSIC_SUITE_STATE_PLAYING = 1
MUSIC_SUITE_STATE_PAUSED = 2
MUSIC_SUITE_STATE_OFF = 0

class ActionDict():
  def __init__(self, camera):
    self.actionLambdaDict = (
      { "clickCameraSnap":  lambda: drag("820x240,820x240")
      , "clickCameraFocus": lambda: drag("820x240-820x100*200+5")
      , "torchOn":          lambda: camera.torchOn()
      , "torchOff":         lambda: camera.torchOff()
      , "torchToggle":      lambda: camera.torchToggle()
      , "cmd":              lambda cmd: lambda: shellCmd(cmd)
      , "musicPlayPause":   lambda: musicPlayPause()
      , "musicNext":        lambda: musicSuiteDbus("next")
      , "musicPrev":        lambda: musicSuiteDbus("previous")
      , "screenShot":       lambda: screenShot()
      })

    self.conditionLambdaDict = (
      { "screenLocked": lambda: QSystemDeviceInfo().isDeviceLocked()
      , "cameraAppFocused": lambda: isAppOnTop("camera-ui")
      , "appFocused": lambda x: lambda: isAppOnTop(x)
      , "always": lambda: True
      })

  def getActionLambdaDict(self):
    return self.actionLambdaDict
  def getConditionLambdaDict(self):
    return self.conditionLambdaDict

###############

def isAppOnTop(app):
  winId = readProc(["xprop", "-root", "_NET_ACTIVE_WINDOW"]) [40:]
  winCmd = readProc(["xprop", "-id", winId, "WM_COMMAND"]) [24:-4]
  return app in winCmd

def musicPlayPause():
  state = musicSuiteDbus("playbackState")
  try:
    state = int(state.strip())
  except e:
    print >> sys.stderr, "ERROR READING MUSIC SUITE STATE: " + str(e)

  if state == MUSIC_SUITE_STATE_PLAYING:
    musicSuiteDbus("pausePlayback")
  elif state == MUSIC_SUITE_STATE_PAUSED:
    musicSuiteDbus("resumePlayback")

def musicSuiteDbus(methodShortName):
  servicename = "com.nokia.maemo.meegotouch.MusicSuiteService"
  path = "/"
  method = "com.nokia.maemo.meegotouch.MusicSuiteInterface." + methodShortName
  return readProc(["qdbus", servicename, path, method])

def drag(arg):
  runcmd(["xresponse", "-w", "1", "-d", arg])

def screenShot():
  millis = int(round(time.time() * 1000))
  fileName = SCREENSHOT_DIR + "/screenshot_" + str(millis) + ".png"

  ss = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
  rot90 = QtGui.QTransform().rotate(90)
  ss = ss.toImage().transformed(rot90)
  ss.save(fileName, "png")

def shellCmd(cmd):
  runcmd(['sh', '-c', cmd])

def runcmd(cmdArr):
  print 'running cmd: "' + ' '.join(cmdArr) + '"'
  subprocess.Popen(cmdArr)

def readProc(cmdArr):
  print 'running cmd: "' + ' '.join(cmdArr) + '"'
  out, err = subprocess.Popen(cmdArr, stdout=subprocess.PIPE).communicate()
  return out

