#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide.QtGui import QWidget
from PySide.QtCore import QBasicTimer
from QtMobility.MultimediaKit import (QCamera, QCameraExposure)

import time
import sys
import subprocess

class TorchAutoShutOff(QWidget):
  def __init__(self, camera):
    super(TorchAutoShutOff, self).__init__()
    self.camera = camera
    self.timer = QBasicTimer()
  def schedule(self, time):
    self.timer.start(time, self)
  def cancel(self):
    self.timer.stop()
  def timerEvent(self, e):
    self.timer.stop()
    if self.camera.torchState == "on":
      print "auto shut-off"
      self.camera.torchOff()

class Camera():
  def __init__(self):
    self.torchState = "off"

  def setConfig(self, config):
    self.config = config

  def initCamera(self):
    self.qcam = QCamera()
    self.autoShutOff = TorchAutoShutOff(self)
    self.on()
    self.autoShutOff.schedule(500)

  def torchToggle(self):
    if self.torchState == "on":
      self.torchOff()
    else:
      self.torchOn()

  def torchOn(self):
    print "torch on"
    self.qcam.setCaptureMode(QCamera.CaptureVideo)
    self.qcam.exposure().setFlashMode(QCameraExposure.FlashTorch)
    self.qcam.start()
    self.torchState = "on"
    if self.config != None and self.config.torchAutoShutOffTimeMs != None:
      self.autoShutOff.schedule(self.config.torchAutoShutOffTimeMs)

  def torchOff(self):
    self.autoShutOff.cancel()
    print "torch off"
    self.qcam.setCaptureMode(QCamera.CaptureStillImage)
    self.qcam.exposure().setFlashMode(QCameraExposure.FlashManual)
    self.qcam.unlock()
    self.qcam.unload()
    self.torchState = "off"