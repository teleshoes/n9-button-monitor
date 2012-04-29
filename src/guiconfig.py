#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from config import Config, ActionMap
from actions import ActionDict
from clicktimer import getButtons, getClickTypes

from PySide.QtGui import *

import sys

class GuiConfig(QMainWindow):
  def __init__(self):
    self.actionDict = ActionDict(None)

    self.config = Config(
      self.actionDict,
      getButtons().keys(),
      getClickTypes())
  def showGui(self):
    app = QApplication([])
    table = ActionTable(self.actionDict)
    table.addRow()
    table.getWidget().show()
    app.exec_()

class ActionTable():
  def __init__(self, actionDict):
    self.actionDict = actionDict
    self.table = QTableWidget(0, 6)
    self.table.setHorizontalHeaderLabels([
      "Button", "Click Type",
      "Action Name", "Action Param",
      "Condition Name", "Condition Param"])
    self.loadConfig()
  def getWidget(self):
    return self.table
  def loadConfig(self):
    config = Config(self.actionDict, getButtons().keys(), getClickTypes())
    config.parse()
    for actionMap in config.getActionMapSet().actionMaps:
      self.addRow(actionMap)
  def addRow(self, actionMap=None):
    r = self.table.rowCount()
    self.table.setRowCount(r+1)
    row = ActionRow(self.actionDict)
    self.table.setCellWidget(r, 0, row.buttonBox)
    self.table.setCellWidget(r, 1, row.clickTypeBox)
    self.table.setCellWidget(r, 2, row.actionNameBox)
    self.table.setCellWidget(r, 3, row.actionParamBox)
    self.table.setCellWidget(r, 4, row.conditionNameBox)
    self.table.setCellWidget(r, 5, row.conditionParamBox)
    if actionMap != None:
      row.setActionMap(actionMap)

class ActionRow():
  def __init__(self, actionDict):
    self.actionDict = actionDict

    self.buttonBox = self.makeComboBox(getButtons().keys())
    self.clickTypeBox = self.makeComboBox(getClickTypes())
    self.actionNameBox = self.makeComboBox(
      self.actionDict.getActionLambdaDict().keys())
    self.actionParamBox = QLineEdit()
    self.conditionNameBox = self.makeComboBox(
      self.actionDict.getConditionLambdaDict().keys())
    self.conditionParamBox = QLineEdit()

    self.connectComboBox(self.buttonBox, self.setButtonIndex)
    self.connectComboBox(self.clickTypeBox, self.setClickTypeIndex)
    self.connectComboBox(self.actionNameBox, self.setActionNameIndex)
    self.connectComboBox(self.conditionNameBox, self.setConditionNameIndex)

  def connectComboBox(self, cb, func):
    cb.currentIndexChanged.connect(func)

  def setActionMap(self, actionMap):
    self.setComboBoxByText(self.buttonBox, actionMap.button)
    self.setComboBoxByText(self.clickTypeBox, actionMap.clickType)
    self.setComboBoxByText(self.actionNameBox, actionMap.actionName)
    self.actionParamBox.setText(actionMap.actionParam)
    self.setComboBoxByText(self.conditionNameBox, actionMap.condName)
    self.conditionParamBox.setText(actionMap.condParam)

  def setComboBoxByText(self, cb, text):
    for i in range(cb.count()):
      if cb.itemText(i) == text:
        cb.setCurrentIndex(i)
        return

  def setButtonIndex(self, index):
    self.button = self.buttonBox.itemText(index)
  def setClickTypeIndex(self, index):
    self.clickType = self.clickTypeBox.itemText(index)
  def setActionNameIndex(self, index):
    self.actionName = self.actionNameBox.itemText(index)
  def setConditionNameIndex(self, index):
    self.conditionName = self.conditionNameBox.itemText(index)
  
  def getButton(self):
    return self.button
  def getClickType(self):
    return self.clickType
  def getActionName(self):
    return self.actionName
  def getActionParam(self):
    return self.actionParamBox.getText()
  def getCondition(self):
    return self.conditionName
  def getConditionParam(self):
    return self.conditionParamBox.getText()

  def makeComboBox(self, items):
    cb = QComboBox()
    cb.addItems(items)
    return cb
