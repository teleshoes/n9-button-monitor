#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from clicktimer import getButtons

import sys
import os
import re

configFilePath = "/home/user/.config/n9-button-monitor.ini"
defaultConfig = (
"""#DEFAULT CONFIG
torchAutoShutOffTimeMs=30000
longClickDelayMs=400
doubleClickDelayMs=400
trebleClickDelayMs=600
action=torchOn,volumeUp,longClickStart,screenLocked
action=torchOff,volumeUp,longClickStop,screenLocked
action=cameraFocus,volumeUp,longClickStart,cameraAppFocused
action=cameraSnap,volumeUp,longClickStop,cameraAppFocused
action=cameraSnap,volumeUp,singleClick,cameraAppFocused
""")

class Config():
  def __init__(self, actionDict, validButtonNames, validClickTypeNames):
    self.actionDict = actionDict
    self.validActionNames = actionDict.getActionLambdaDict().keys()
    self.validConditionNames = actionDict.getConditionLambdaDict().keys()
    self.validButtonNames = validButtonNames
    self.validClickTypeNames = validClickTypeNames
    self.resetConfig()

  def resetConfig(self):
    self.torchAutoShutOffTimeMs=300000
    self.longClickDelayMs=400
    self.doubleClickDelayMs=400
    self.trebleClickDelayMs=600
    self.actionMaps = []
    self.actionMapSet = ActionMapSet()

  def getIntFieldRegex(self, fieldName):
    return re.compile("^" + fieldName + "=" + "(\d+)" + "$")
  def getActionMapRegex(self):
    return re.compile(""
      + "^"
      + "\\s*action\\s*=\\s*"
      + "(?P<actionName>" + "|".join(self.validActionNames) + ")"
      + "(?:" + "\(" + "(?P<actionParam>[^)]*)" + "\)" + ")?"
      + "\\s*,\\s*"
      + "(?P<button>" + "|".join(self.validButtonNames) + ")"
      + "\\s*,\\s*"
      + "(?P<clickType>" + "|".join(self.validClickTypeNames) + ")"
      + "\\s*,\\s*"
      + "(?P<condName>" + "|".join(self.validConditionNames) + ")"
      + "(?:" + "\(" + "(?P<condParam>[^)]*)" + "\)" + ")?"
      + "\\s*(#.*)?"
      + "$"
      )
  def parse(self):
    self.resetConfig()
    if os.path.isfile(configFilePath):
      confText = open(configFilePath,"rb").read()
    else:
      confText = defaultConfig
      print "WARNING: no config file at '" + configFilePath + "'"
      print "Using default config:\n" + confText
    self.parse(confText)
  def parse(self, confText):
    actionMapRe = self.getActionMapRegex()
    integerRe = re.compile(
      "^\\s*(?P<key>[a-zA-Z0-9]+)" + "\\s*=\\s*" + "(?P<value>\d+)\\s*(#.*)?$")
    commentRe = re.compile("^\\s*#.*$")
    emptyRe = re.compile("^\\s*$")
    for line in confText.splitlines():
      actionMapMatch = actionMapRe.match(line)
      integerMatch = integerRe.match(line)
      commentMatch = commentRe.match(line)
      emptyMatch = emptyRe.match(line)
      key = None
      if integerMatch != None:
        key = integerMatch.group("key")
        val = int(integerMatch.group("value"))

      if actionMapMatch != None:
        self.actionMaps.append(ActionMap(
          self.actionDict,
          actionName = actionMapMatch.group("actionName"),
          actionParam = actionMapMatch.group("actionParam"),
          condName = actionMapMatch.group("condName"),
          condParam = actionMapMatch.group("condParam"),
          button = actionMapMatch.group("button"),
          clickType = actionMapMatch.group("clickType"),
        ))
      elif key == "torchAutoShutOffTimeMs":
        self.torchAutoShutOffTimeMs = val
      elif key == "longClickDelayMs":
        self.longClickDelayMs = val
      elif key == "doubleClickDelayMs":
        self.doubleClickDelayMs = val
      elif key == "trebleClickDelayMs":
        self.trebleClickDelayMs = val
      elif commentMatch == None and emptyMatch == None:
        print >> sys.stderr, "Unparseable config entry: " + line
        raise Exception("Unparseable config entry: " + line)
    self.actionMapSet.setActionMaps(self.actionMaps)
  def getActionMapSet(self):
    return self.actionMapSet

class ActionMapSet():
  def setActionMaps(self, actionMaps):
    self.actionMaps = actionMaps
    self.actionMapsByKeyByClickType = dict()
    for a in actionMaps:
      if not a.clickType in self.actionMapsByKeyByClickType:
        self.actionMapsByKeyByClickType[a.clickType] = dict()
      actionMapsByKey = self.actionMapsByKeyByClickType[a.clickType]
      if not a.key in actionMapsByKey:
        actionMapsByKey[a.key] = []
      actionMapsByKey[a.key].append(a)
  def getActionMaps(self, key, clickType):
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
               button, clickType):
    self.actionName = actionName
    self.actionParam = actionParam
    self.condName = condName
    self.condParam = condParam
    self.button = button
    self.key = getButtons()[button]
    self.clickType = clickType
    
    self.actionLambda = self.getLambda(actionDict.getActionLambdaDict(),
      self.actionName, self.actionParam)
    self.condLambda = self.getLambda(actionDict.getConditionLambdaDict(),
      self.condName, self.condParam)
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

