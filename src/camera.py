#!/usr/bin/python
#N9 Button Monitor
#Copyright (C) 2012 Elliot Wolk
#Copyright (C) 2013 Lcferrum
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PySide.QtGui import QWidget
from PySide.QtCore import QBasicTimer
from QtMobility.MultimediaKit import (
  QCamera, QCameraExposure, QCameraImageCapture)

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
    if self.config != None and self.config.cameraDisabled != 1:
      self.qcam = QCamera()
      self.qcam.locked.connect(self.snap)

      self.imgCapture = QCameraImageCapture(self.qcam)
      self.imgCapture.imageSaved.connect(self.pictureSaved)
      self.imgCapture.error.connect(self.error)

      self.autoShutOff = TorchAutoShutOff(self)
      self.autoShutOff.schedule(500)

  def setFlashMode(self, mode):
    self.qcam.exposure().setFlashMode(
      { "auto":   QCameraExposure.FlashAuto
      , "manual": QCameraExposure.FlashManual
      , "on":     QCameraExposure.FlashOn
      , "off":    QCameraExposure.FlashOff
      , "torch":  QCameraExposure.FlashTorch
      }[mode])

  def focusAndSnap(self, flashMode):
    if self.config != None and self.config.cameraDisabled != 1:
      self.qcam.setCaptureMode(QCamera.CaptureStillImage)
      self.qcam.start()
      self.setFlashMode(flashMode)
      self.qcam.searchAndLock()

  def snap(self):
    self.imgCapture.capture(self.getPictureFile())

  def pictureSaved(self, picId, picFilename):
    print >>sys.stderr, 'saved picture: ' + picFilename
    self.playSound()
    self.unloadCamera()

  def error(self, errId, err, errStr):
    print >>sys.stderr, "error: " + errStr
    self.unloadCamera()

  def unloadCamera(self):
    self.qcam.unlock()
    self.qcam.unload()

  def getPictureFile(self):
    millis = int(round(time.time() * 1000))
    return "/home/user/MyDocs/DCIM/" + str(millis) + ".jpg"

  def getSoundFile(self):
    return "/usr/share/sounds/ui-tones/snd_camera_shutter.wav"

  def playSound(self):
    subprocess.Popen(["aplay", self.getSoundFile()])

  def torchToggle(self):
    if self.torchState == "on":
      self.torchOff()
    else:
      self.torchOn()

  def torchOn(self):
    if self.config != None and self.config.cameraDisabled != 1:
      print "torch on"
      self.qcam.setCaptureMode(QCamera.CaptureVideo)
      self.setFlashMode("torch")
      self.qcam.start()
      self.torchState = "on"
      if self.config != None and self.config.torchAutoShutOffTimeMs != None:
        self.autoShutOff.schedule(self.config.torchAutoShutOffTimeMs)

  def torchOff(self):
    if self.config != None and self.config.cameraDisabled != 1:
      self.autoShutOff.cancel()
      print "torch off"
      self.qcam.setCaptureMode(QCamera.CaptureStillImage)
      self.setFlashMode("manual")
      self.unloadCamera()
      self.torchState = "off"
