#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from config import Config
from actions import ActionSet
from clicktimer import ClickTimer, getButtons, getClickTypes
from torch import Torch

from QmSystem import QmKeys
from PySide.QtGui import QApplication
from QtMobility.SystemInfo import QSystemDeviceInfo

import sys
import re
import time
import subprocess

def main():
  actionSet = ActionSet()

  config = Config(
    actionSet.getActionNames(), actionSet.getCondNames(),
    getButtons().keys(), getClickTypes())
  
  config.parse()

  torch = Torch(config.torchAutoShutOffTimeMs)

  config.initLambdas(
    actionSet.getActionLambdaDict(torch),
    actionSet.getCondLambdaDict()
  )

  app = QApplication(sys.argv)
  torch.initCamera()
  keys = QmKeys()
  buttonTimers = dict()
  for b in getButtons().values():
    buttonTimers[b] = ClickTimer(b, config)
  keys.keyEvent.connect(lambda k, s:
    (k in buttonTimers and buttonTimers[k].keyEvent(s)))
  app.exec_()

if __name__ == "__main__":
  sys.exit(main())

