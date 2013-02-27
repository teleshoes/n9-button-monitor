#N9 Button Monitor
#Copyright (C) 2013 Elliot Wolk, Lcferrum
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

APP_NAME = n9-button-monitor
SOURCE = src
DATA = data

DEST_BIN = $(DESTDIR)/opt/$(APP_NAME)/bin/
DEST_DATA = $(DESTDIR)/opt/$(APP_NAME)/data/
DEST_ICONS = $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/
DEST_DESKTOP = $(DESTDIR)/usr/share/applications/
DEST_UPSTART = $(DESTDIR)/etc/init/apps/

all:
	true

install:
	mkdir -p $(DEST_BIN)
	mkdir -p $(DEST_DATA)
	mkdir -p $(DEST_ICONS)
	mkdir -p $(DEST_UPSTART)
	mkdir -p $(DEST_DESKTOP)
	cp $(SOURCE)/*.py $(DEST_BIN)
	cp $(DATA)/*.desktop $(DEST_DESKTOP)
	cp $(DATA)/$(APP_NAME).conf $(DEST_UPSTART)

.PHONY: all install

