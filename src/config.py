#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from actions import ActionMap
from clicktimer import getButtons

import sys
import os
import re

configFilePath = "/home/user/.config/n9-button-monitor.ini"
deprecatedConfigFilePath = "/home/user/.config/n9-button-monitor.conf"

class Config():
  def __init__(self,
               validActionNames, validConditionNames,
               validButtonNames, validClickTypeNames):
    self.validActionNames = validActionNames
    self.validConditionNames = validConditionNames
    self.validButtonNames = validButtonNames
    self.validClickTypeNames = validClickTypeNames
    self.torchAutoShutOffTimeMs=300000
    self.longClickDelayMs=400
    self.doubleClickDelayMs=400
    self.trebleClickDelayMs=600
    self.actionMaps = []
  def initLambdas(self, actionLambdaDict, condLambdaDict):
    for actionMap in self.actionMaps:
      actionMap.initLambdas(actionLambdaDict, condLambdaDict)
  def getDefaultConfig(self):
    return (""
      + "#DEFAULT CONFIG\n"
      + "torchAutoShutOffTimeMs=30000\n"
      + "longClickDelayMs=400\n"
      + "doubleClickDelayMs=400\n"
      + "trebleClickDelayMs=600\n"
      + "action=torchOn,volumeUp,longClickStart,screenLocked\n"
      + "action=torchOff,volumeUp,longClickStop,screenLocked\n"
      + "action=cameraFocus,volumeUp,longClickStart,cameraAppFocused\n"
      + "action=cameraSnap,volumeUp,longClickStop,cameraAppFocused\n"
      + "action=cameraSnap,volumeUp,singleClick,cameraAppFocused\n"
      )
  def getIntFieldRegex(self, fieldName):
    return re.compile("^" + fieldName + "=" + "(\d+)" + "$")
  def getActionMapRegex(self):
    ptrn = (""
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
    return re.compile(ptrn)
  def parse(self):
    if os.path.isfile(configFilePath):
      config = open(configFilePath,"rb").read()
    elif os.path.isfile(deprecatedConfigFilePath):
      config = open(deprecatedConfigFilePath,"rb").read()
      print ("WARNING: config file should be '" + configFilePath + "'\n" +
             "{not '" + deprecatedConfigFilePath + "'}")
    else:
      config = self.getDefaultConfig()
      print "WARNING: no config file at '" + configFilePath + "'"
      print "Using default config:\n" + config

    actionMapRe = self.getActionMapRegex()
    integerRe = re.compile(
      "^\\s*(?P<key>[a-zA-Z0-9]+)" + "\\s*=\\s*" + "(?P<value>\d+)\\s*(#.*)?$")
    commentRe = re.compile("^\\s*#.*$")
    emptyRe = re.compile("^\\s*$")
    for line in config.splitlines():
      actionMapMatch = actionMapRe.match(line)
      integerMatch = integerRe.match(line)
      commentMatch = commentRe.match(line)
      emptyMatch = emptyRe.match(line)
      key = None
      if integerMatch != None:
        key = integerMatch.group("key")
        val = int(integerMatch.group("value"))

      if commentMatch != None or emptyMatch != None:
        pass
      elif actionMapMatch != None:
        self.actionMaps.append(ActionMap(
          actionName = actionMapMatch.group("actionName"),
          actionParam = actionMapMatch.group("actionParam"),
          condName = actionMapMatch.group("condName"),
          condParam = actionMapMatch.group("condParam"),
          key = getButtons()[actionMapMatch.group("button")],
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
      else:
        print >> sys.stderr, "Unparseable config entry: " + line
        sys.exit(1)

