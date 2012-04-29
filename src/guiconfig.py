#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from config import Config, ActionMap, getConfigFilePath
from actions import ActionDict
from clicktimer import getButtons, getClickTypes

from PySide.QtGui import *

import datetime
import sys
from time import sleep

class GuiConfig():
  def __init__(self):
    self.actionDict = ActionDict(None)
    self.config = Config(self.actionDict, getButtons().keys(), getClickTypes())
    self.configPanel = ConfigPanel(self.actionDict)
  def createButtonPanel(self):
    panel = QHBoxLayout()
    panel.addWidget(self.makeButton("Load Config File", self.loadConfigFile))
    panel.addWidget(self.makeButton("Load Default Config",
      self.loadConfigDefault))
    panel.addWidget(self.makeButton("Save Config File", self.saveConfig))
    return panel
  def makeButton(self, label, clickFunc):
    btn = QPushButton(label)
    btn.clicked.connect(clickFunc)
    return btn
    
  def showGui(self):
    app = QApplication([])

    self.configPanel.initUI()
    
    mainPanel = QVBoxLayout()
    mainPanel.addLayout(self.createButtonPanel())
    mainPanel.addLayout(self.configPanel)

    widget = QWidget()
    widget.setLayout(mainPanel)
    widget.show()
    app.exec_()
  def loadConfigFile(self):
    confText = self.config.getConfigFileContent()
    if confText == None:
      msgBox = QMessageBox()
      msgBox.setText("Config file not found!")
      msgBox.exec_()
    else:
      self.loadConfig(confText)
  def loadConfigDefault(self):
    self.loadConfig(self.config.getDefaultConfig())
  def loadConfig(self, confText):
    try:
      self.config.parse(confText)
    except:
      msgBox = QMessageBox()
      msgBox.setText("Could not parse config:\n" + str(sys.exc_info()[1]) +
        "\n\n" + confText)
      msgBox.exec_()
      raise
    else:
      self.configPanel.applyConfig(self.config)
  
  def saveConfig(self):
    confText = self.configPanel.makeConfigText()
    self.loadConfig(confText)
    open(getConfigFilePath(), 'w').write(confText)
    
    
class ConfigPanel(QVBoxLayout):
  def __init__(self, actionDict):
    QVBoxLayout.__init__(self)
    self.actionDict = actionDict
  def initUI(self):
    self.actionTable = ActionTable(self.actionDict)
    self.actionTable.initUI()

    self.torchAutoShutOffTimeMsNumBox = NumBox("Torch Auto-shutoff (ms): ")
    self.longClickDelayMsNumBox = NumBox("Long-click Delay (ms): ")
    self.doubleClickDelayMsNumBox = NumBox("Double-click Delay (ms): ")
    self.trebleClickDelayMsNumBox = NumBox("Treble-click Delay (ms): ")
    self.addLayout(self.torchAutoShutOffTimeMsNumBox)
    self.addLayout(self.longClickDelayMsNumBox)
    self.addLayout(self.doubleClickDelayMsNumBox)
    self.addLayout(self.trebleClickDelayMsNumBox)

    self.addWidget(self.actionTable.getWidget())
  def applyConfig(self, config):
    self.torchAutoShutOffTimeMsNumBox.setVal(config.torchAutoShutOffTimeMs)
    self.longClickDelayMsNumBox.setVal(config.longClickDelayMs)
    self.doubleClickDelayMsNumBox.setVal(config.doubleClickDelayMs)
    self.trebleClickDelayMsNumBox.setVal(config.trebleClickDelayMs)
    self.actionTable.clear()
    for actionMap in config.getActionMapSet().actionMaps:
      self.actionTable.addRow(actionMap)
  def makeConfigText(self):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return ("#autogenerated on " + date + "\n"
      + "torchAutoShutOffTimeMs="
        + str(self.torchAutoShutOffTimeMsNumBox.getVal()) + "\n"
      + "longClickDelayMs="
        + str(self.longClickDelayMsNumBox.getVal()) + "\n"
      + "doubleClickDelayMs="
        + str(self.doubleClickDelayMsNumBox.getVal()) + "\n"
      + "trebleClickDelayMs="
        + str(self.trebleClickDelayMsNumBox.getVal()) + "\n"
      + self.actionTable.formatActionRows()
      )
  def clear(self):
    self.actionTable.clear()

class NumBox(QHBoxLayout):
  def __init__(self, label):
    QHBoxLayout.__init__(self)
    self.label = QLabel(label)
    self.textBox = QLineEdit()
    self.addWidget(self.label)
    self.addWidget(self.textBox)
    self.textBox.setInputMask('99999999999999999999')
  def getVal(self):
    try:
      return int(self.textBox.text())
    except:
      return 0
  def setVal(self, val):
    return self.textBox.setText(str(val))

class ActionTable():
  def __init__(self, actionDict):
    self.actionDict = actionDict
    self.actionRows = []
  def initUI(self):
    self.table = QTableWidget(0, 6)
    self.table.setHorizontalHeaderLabels([
      "Button", "Click Type",
      "Action Name", "Action Param",
      "Condition Name", "Condition Param"])
  def getWidget(self):
    return self.table
  def clear(self):
    self.actionRows = []
    self.table.setRowCount(0)
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
    self.actionRows.append(row)
    if actionMap != None:
      row.setActionMap(actionMap)
  def formatActionRows(self):
    str = ''
    for actionRow in self.actionRows:
      str += actionRow.format()
    return str
      

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

    self.setButtonIndex(0)
    self.setClickTypeIndex(0)
    self.setActionNameIndex(0)
    self.setConditionNameIndex(0)

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
  
  def format(self):
    actionParam = self.actionParamBox.text()
    if actionParam != None and len(actionParam) > 0:
      actionParam = "(" + actionParam + ")"
    else:
      actionParam = ""
    
    conditionParam = self.conditionParamBox.text()
    if conditionParam != None and len(conditionParam) > 0:
      conditionParam = "(" + conditionParam + ")"
    else:
      conditionParam = ""
    
    return ("action="
      + self.actionName + actionParam + ","
      + self.button + ","
      + self.clickType + ","
      + self.conditionName + conditionParam
      + "\n")

  def makeComboBox(self, items):
    cb = QComboBox()
    cb.addItems(items)
    return cb