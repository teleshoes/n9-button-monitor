#!/usr/bin/python
#N9 LED Control
#Copyright (C) 2013 Elliot Wolk
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import string
import subprocess
import sys
import time

actions = (''
  + "  <###>led: set led brightness to <###> [0-255] {requires led-dbus}\n"
  + "  <###>ms: delay <###> milliseconds\n"
  + "  on: 255led synonym\n"
  + "  off: 0led synonym\n"
)

macros = { 'blink': 'on, 10ms, off'
         , 'doubleblink': 'on, 10ms, off, 100ms, on, 10ms, off'
         }

class LedPattern():
  def __init__(self, ptrnStr):
    if ptrnStr in macros:
      ptrnStr = macros[ptrnStr]
    self.pattern = []
    for item in ptrnStr.split(','):
      action = self.getAction(item.strip())
      if action != None:
        self.pattern.append(action)
  def fire(self):
    for action in self.pattern:
      action()
  def getAction(self, actionStr):
    ledMatch = re.match('^([0-9]+)led$', actionStr)
    msMatch = re.match('^([0-9]+)ms$', actionStr)
    if ledMatch != None:
      brightness = int(ledMatch.group(1))
      if 0 <= brightness and brightness <= 255:
        return lambda: self.led(int(ledMatch.group(1)))
      else:
        print >> sys.stderr, 'led pattern brightness goes from 0 to 255'
    elif msMatch != None:
      return lambda: self.sleep(int(msMatch.group(1)))
    elif actionStr.lower() == "on":
      return lambda: self.led(255)
    elif actionStr.lower() == "off":
      return lambda: self.led(0)

    print >> sys.stderr, "invalid action: " + actionStr + "\n" + actions
  def sleep(self, millis):
    time.sleep(millis/1000.0)
  def led(self, brightness):
    cmd = ['qdbus', 'org.teleshoes.led', '/', 'led', str(brightness)]
    subprocess.call(cmd)

def main():
  LedPattern(string.join(sys.argv[1:], ', ')).fire()

if __name__ == "__main__":
  sys.exit(main())
