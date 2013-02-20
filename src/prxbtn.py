#!/usr/bin/python
#N9 Button Monitor
#Copyright (C) 2013 Lcferrum
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import signal

from PySide.QtCore import QCoreApplication
from QtMobility import Sensors

signal.signal(signal.SIGINT, signal.SIG_DFL)

class ProximityFilter(Sensors.QProximityFilter):
	def __init__(self, eventHandler):
 		super(ProximityFilter, self).__init__()
		self.eventHandler = eventHandler
	def filter(self, reading):
		self.eventHandler(reading.close())
		return False

class ProximityButton():
	def __init__(self):
		self.handler = self.defaultHandler
		self.last_close = False
	def defaultHandler(self, state):
		print >> sys.stderr, "Proximity sensor event: " + state
	def setHandler(self, handler):
		self.handler = handler
	def proximityEvent(self, close):
		if close != self.last_close:
			if close:
				self.handler("proximityEnter")
			else:
				self.handler("proximityLeave")
			self.last_close = close
	def connectProximityButton(self):
		self.prox = Sensors.QProximitySensor()
		self.filter = ProximityFilter(self.proximityEvent)
		self.prox.addFilter(self.filter)
		self.prox.start()
		if not self.prox.isActive():
			print >> sys.stderr, "Proximity sensor didn't start!"
			sys.exit(1)

if __name__ == '__main__':
	app = QCoreApplication([])
	ProximityButton().connectProximityButton()
	app.exec_()
