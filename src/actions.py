#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from QtMobility.SystemInfo import QSystemDeviceInfo

import sys
import subprocess

MUSIC_SUITE_STATE_PLAYING = 1
MUSIC_SUITE_STATE_PAUSED = 2
MUSIC_SUITE_STATE_OFF = 0

class ActionSet():
  def getActionLambdaDict(self, torch):
    return getActionLambdaDict(torch)
  def getActionNames(self):
    return self.getActionLambdaDict(None).keys()
  def getCondLambdaDict(self):
    return getCondLambdaDict()
  def getCondNames(self):
    return self.getCondLambdaDict().keys()

class ActionMap():
  def __init__(self, actionName, actionParam,
               condName, condParam, key, clickType):
    self.actionName = actionName
    self.actionParam = actionParam
    self.condName = condName
    self.condParam = condParam
    self.key = key
    self.clickType = clickType
  def initLambdas(self, actionLambdaDict, condLambdaDict):
    self.actionLambda = self.getLambda(
      actionLambdaDict, self.actionName, self.actionParam)
    self.condLambda = self.getLambda(
      condLambdaDict, self.condName, self.condParam)
  def __str__(self):
    if self.actionParam == None:
      param = ""
    else:
      param = "(" + self.actionParam + ")"
    action = self.actionName + param
    return (str(self.key) + "[" + self.clickType + "]: " + action)
  def getLambda(self, lambdaDict, lambdaName, lambdaParam):
    lam = lambdaDict[lambdaName]
    assert self.isLambda(lam), "'" + lambdaName + "' not defined"
    if lambdaParam != None:
      try:
        lam = lam(lambdaParam)
        assert self.isLambda(lam)
      except:
        print >> sys.stderr, (
          "'" + lambdaName + "' does not accept an argument\n" +
          "{given: '" + lambdaParam + "'}")
        sys.exit(1)
    return lam
  def isLambda(self, v):
    return isinstance(v, type(lambda: None)) and v.__name__ == '<lambda>'

###############

def getCondLambdaDict():
  return { "screenLocked": lambda: QSystemDeviceInfo().isDeviceLocked()
         , "cameraAppFocused": lambda: isAppOnTop("camera-ui")
         , "appFocused": lambda x: lambda: isAppOnTop(x)
         }

def isAppOnTop(app):
  winId = readProc(["xprop", "-root", "_NET_ACTIVE_WINDOW"]) [40:]
  winCmd = readProc(["xprop", "-id", winId, "WM_COMMAND"]) [24:-4]
  return app in winCmd

###############

def getActionLambdaDict(torch):
  return { "cameraSnap": lambda: drag("820x240,820x240")
         , "cameraFocus": lambda: drag("820x240-820x100*200+5")
         , "torchOn": lambda: torch.on()
         , "torchOff": lambda: torch.off()
         , "torchToggle": lambda: torch.toggle()
         , "cmd": lambda x: lambda: shellCmd(x)
         , "drag": lambda x: lambda: drag
         , "musicPlayPause": lambda: musicPlayPause()
         , "musicNext": lambda: musicSuiteDbus("next")
         , "musicPrev": lambda: musicSuiteDbus("previous")
         }

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

###############

def shellCmd(cmd):
  runcmd(['sh', '-c', cmd])

def runcmd(cmdArr):
  print 'running cmd: "' + ' '.join(cmdArr) + '"'
  subprocess.Popen(cmdArr)

def readProc(cmdArr):
  print 'running cmd: "' + ' '.join(cmdArr) + '"'
  out, err = subprocess.Popen(cmdArr, stdout=subprocess.PIPE).communicate()
  return out

###############
