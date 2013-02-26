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

all:
	true

install:
	mkdir -p $(DESTDIR)/opt/$(APP_NAME)/
	mkdir -p $(DESTDIR)/opt/$(APP_NAME)/bin/
	mkdir -p $(DESTDIR)/opt/$(APP_NAME)/data/
	cp $(SOURCE)/*.sh $(SOURCE)/*.py $(DESTDIR)/opt/$(APP_NAME)/bin/
	cp $(DATA)/off.desktop $(DESTDIR)/opt/$(APP_NAME)/data/
	cp $(DATA)/on.desktop $(DESTDIR)/opt/$(APP_NAME)/data/
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp $(DATA)/$(APP_NAME).desktop $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/
	cp $(DATA)/*.png $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/

.PHONY: all install

