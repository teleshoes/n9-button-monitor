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

from ledpattern import LedPattern
from clicktimer import getButtons
from dbusbtn import DbusButton
from prxbtn import ProximityButton

import sys
import os
import re
import subprocess

CAMERA_SOUND = "/usr/share/sounds/ui-tones/snd_camera_shutter.wav"

def getUserConfigFilePath():
  return "/home/user/.config/n9-button-monitor.ini"
def getSystemConfigFilePath():
  return "/opt/n9-button-monitor/data/default-config.ini"

class Config():
  def __init__(self, actionDict, validButtonNames, validClickTypeNames):
    self.actionDict = actionDict
    self.validActionNames = actionDict.getActionLambdaDict().keys()
    self.validConditionNames = actionDict.getConditionLambdaDict().keys()
    self.validButtonNames = validButtonNames
    self.validClickTypeNames = validClickTypeNames
    self.dbusButton = DbusButton()
    self.proximityButton = ProximityButton()
    self.lastTimeStamp = None
    self.resetConfig()
    self.initRegex()
  def checkConfigFile(self):
    timestamp = self.getTimeStamp()
    if self.lastTimeStamp == None or self.lastTimeStamp != timestamp:
      print >> sys.stderr, "refreshing config"
      self.ensureUserConf()
      try:
        self.parse(self.readConf(getUserConfigFilePath()))
      except:
        print >> sys.stderr, "INVALID CONFIG, ATTEMPTING TO USE DEFAULT"
        self.parse(self.readConf(getSystemConfigFilePath()))
    self.lastTimeStamp = timestamp
  def getTimeStamp(self):
    if os.path.isfile(getUserConfigFilePath()):
      cmdArr = ["stat", "-t", getUserConfigFilePath()]
      out, err = subprocess.Popen(cmdArr, stdout=subprocess.PIPE).communicate()
      if err == None or len(err) == 0:
        return out
      else:
        return "error"
    else:
      return "missing"

  def resetConfig(self):
    self.torchAutoShutOffTimeMs=300000
    self.cameraDisabled=0
    self.quickSnapShutterSound=CAMERA_SOUND
    self.quickSnapSaveSound=''
    self.quickSnapShutterLedPattern=LedPattern('blink')
    self.quickSnapSaveLedPattern=LedPattern('doubleblink')
    self.longClickDelayMs=400
    self.doubleClickDelayMs=400
    self.trebleClickDelayMs=600
    self.dbusButton.setPatternDelayMs(1500)
    self.actionMapSet = ActionMapSet([])


  def initRegex(self):
    self.intRe = re.compile(
      "^\\s*(?P<key>[a-zA-Z0-9]+)" + "\\s*=\\s*" + "(?P<value>\d+)\\s*(#.*)?$")
    self.strRe = re.compile(
      "^\\s*(?P<key>[a-zA-Z0-9]+)" + "\\s*=\\s*" + "(?P<value>.*?)\\s*(#.*)?$")
    self.commentRe = re.compile("^\\s*#")
    self.emptyRe = re.compile("^\\s*$")
    self.actionMapRe = re.compile(""
      + "^"
      + "\\s*action\\s*=\\s*"
      + "(?P<actionName>" + "|".join(self.validActionNames) + ")"
      + "(?:" + "\(" + "(?P<actionParam>[^)]*)" + "\)" + ")?"
      + "\\s*,\\s*"
      + "(?P<button>" + "|".join(self.validButtonNames) + ")"
      + "(?:" + "\(" + "(?P<buttonParam>[^)]*)" + "\)" + ")?"
      + "\\s*,\\s*"
      + "(?P<clickType>" + "|".join(self.validClickTypeNames) + ")"
      + "\\s*,\\s*"
      + "(?P<condName>" + "|".join(self.validConditionNames) + ")"
      + "(?:" + "\(" + "(?P<condParam>[^)]*)" + "\)" + ")?"
      + "\\s*(#.*)?"
      + "$"
      )
  def readConf(self, confFile):
    if os.path.isfile(confFile):
      return open(confFile,"rb").read()
    else:
      return None

  def ensureUserConf(self):
    userConf = getUserConfigFilePath()
    if not os.path.isfile(userConf):
      print "WARNING: no config file at '" + userConf + "'"
      print "Copying default config:\n"
      os.system("cp " + getSystemConfigFilePath() + " " + userConf)

  def parse(self, confText):
    self.resetConfig()
    actionMaps = []
    for line in confText.splitlines():
      actionMapMatch = self.actionMapRe.match(line)
      intMatch = self.intRe.match(line)
      strMatch = self.strRe.match(line)
      commentMatch = self.commentRe.match(line)
      emptyMatch = self.emptyRe.match(line)
      intKey = None
      if intMatch != None:
        intKey = intMatch.group("key")
        intVal = int(intMatch.group("value"))
      strKey = None
      if strMatch != None:
        strKey = strMatch.group("key")
        strVal = strMatch.group("value")

      if actionMapMatch != None:
        actionMaps.append(ActionMap(
          self.actionDict,
          actionName = actionMapMatch.group("actionName"),
          actionParam = actionMapMatch.group("actionParam"),
          condName = actionMapMatch.group("condName"),
          condParam = actionMapMatch.group("condParam"),
          button = actionMapMatch.group("button"),
          buttonParam = actionMapMatch.group("buttonParam"),
          clickType = actionMapMatch.group("clickType"),
        ))
      elif intKey == "torchAutoShutOffTimeMs":
        self.torchAutoShutOffTimeMs = intVal
      elif intKey == "cameraDisabled":
        self.cameraDisabled = intVal
      elif intKey == "longClickDelayMs":
        self.longClickDelayMs = intVal
      elif intKey == "doubleClickDelayMs":
        self.doubleClickDelayMs = intVal
      elif intKey == "trebleClickDelayMs":
        self.trebleClickDelayMs = intVal
      elif intKey == "dbusPatternDelayMs":
        self.dbusButton.setPatternDelayMs(intVal)
      elif strKey == "quickSnapShutterSound":
        self.quickSnapShutterSound = strVal
      elif strKey == "quickSnapSaveSound":
        self.quickSnapSaveSound = strVal
      elif strKey == "quickSnapShutterLedPattern":
        self.quickSnapShutterLedPattern = LedPattern(strVal)
      elif strKey == "quickSnapSaveLedPattern":
        self.quickSnapSaveLedPattern = LedPattern(strVal)
      elif commentMatch == None and emptyMatch == None:
        print >> sys.stderr, "Unparseable config entry: " + line
        raise Exception("Unparseable config entry: " + line)
    self.actionMapSet = ActionMapSet(actionMaps)
  def getActionMapSet(self):
    return self.actionMapSet

class ActionMapSet():
  def __init__(self, actionMaps):
    self.actionMaps = actionMaps
    self.actionMapsByDbusButton = dict()
    self.actionMapsByKeyByClickType = dict()
    for a in actionMaps:
      if a.key == a.clickType:
        if a.buttonParam != None:
          if not a.buttonParam in self.actionMapsByKeyByClickType:
            self.actionMapsByKeyByClickType[a.buttonParam] = dict()
          actionMapsByKey = self.actionMapsByKeyByClickType[a.buttonParam]
          if not a.key in actionMapsByKey:
            actionMapsByKey[a.key] = []
          actionMapsByKey[a.key].append(a)
      else:
        if not a.clickType in self.actionMapsByKeyByClickType:
          self.actionMapsByKeyByClickType[a.clickType] = dict()
        actionMapsByKey = self.actionMapsByKeyByClickType[a.clickType]
        if not a.key in actionMapsByKey:
          actionMapsByKey[a.key] = []
        actionMapsByKey[a.key].append(a)
  def getActionMapsForDbus(self, button):
    if not button in self.actionMapsByDbusButton:
      return []
    else:
      return self.actionMapsByDbusButton[button]
  def getActionMapsForKey(self, key, clickType):
    if not clickType in self.actionMapsByKeyByClickType:
      return []
    elif not key in self.actionMapsByKeyByClickType[clickType]:
      return []
    else:
      return self.actionMapsByKeyByClickType[clickType][key]

class ActionMap():
  def __init__(self, actionDict,
               actionName, actionParam,
               condName, condParam,
               button, buttonParam, clickType):
    self.actionName = actionName
    self.actionParam = actionParam
    self.condName = condName
    self.condParam = condParam
    self.button = button
    self.buttonParam = buttonParam
    self.key = getButtons()[button]
    self.clickType = clickType

    self.actionLambda = self.getLambda(actionDict.getActionLambdaDict(),
      self.actionName, self.actionParam)
    self.condLambda = self.getLambda(actionDict.getConditionLambdaDict(),
      self.condName, self.condParam)
  def maybeRun(self):
    if self.condLambda == None or self.condLambda():
      self.actionLambda()
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
        msg = ("'" + lambdaName + "' does not accept an argument\n" +
          "{given: '" + lambdaParam + "'}")
        print >> sys.stderr, msg
        raise Exception(msg)
    return lam
  def isLambda(self, v):
    return isinstance(v, type(lambda: None)) and v.__name__ == '<lambda>'
