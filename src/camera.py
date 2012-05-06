#!/usr/bin/python
#N9 Button Monitor
#Copyright 2012 Elliot Wolk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide.QtGui import QWidget
from PySide.QtCore import QBasicTimer
from QtMobility.MultimediaKit import QCamera, QCameraExposure

class TorchAutoShutOff(QWidget):
  def __init__(self, torch):
    super(TorchAutoShutOff, self).__init__()
    self.torch = torch
    self.timer = QBasicTimer()
  def schedule(self, time):
    self.timer.start(time, self)
  def cancel(self):
    self.timer.stop()
  def timerEvent(self, e):
    self.timer.stop()
    if self.torch.state == "on":
      print "auto shut-off"
      self.torch.off()

class Torch():
  def __init__(self):
    self.state = "off"

  def setConfig(self, config):
    self.config = config

  def initCamera(self):
    self.camera = QCamera()
    self.autoShutOff = TorchAutoShutOff(self)
    self.on()
    self.autoShutOff.schedule(500)

  def toggle(self):
    if self.state == "on":
      self.off()
    else:
      self.on()

  def on(self):
    print "torch on"
    self.camera.setCaptureMode(QCamera.CaptureVideo)
    self.camera.exposure().setFlashMode(QCameraExposure.FlashTorch)
    self.camera.start()
    self.state = "on"
    if self.config != None and self.config.torchAutoShutOffTimeMs != None:
      self.autoShutOff.schedule(self.config.torchAutoShutOffTimeMs)

  def off(self):
    self.autoShutOff.cancel()
    print "torch off"
    self.camera.setCaptureMode(QCamera.CaptureStillImage)
    self.camera.exposure().setFlashMode(QCameraExposure.FlashManual)
    self.camera.unlock()
    self.camera.unload()
    self.state = "off"
