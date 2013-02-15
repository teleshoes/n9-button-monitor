#Advanced Button Monitor
#Copyright 2013 Lcferrum
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

APP_NAME = adv-button-monitor
SOURCE = src

all:
	true

install:
	mkdir -p $(DESTDIR)/opt/$(APP_NAME)/
	cp $(SOURCE)/*.sh $(SOURCE)/*.py $(DESTDIR)/opt/$(APP_NAME)/
	cp $(SOURCE)/off.desktop $(DESTDIR)/opt/$(APP_NAME)/
	cp $(SOURCE)/on.desktop $(DESTDIR)/opt/$(APP_NAME)/
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp $(SOURCE)/$(APP_NAME).desktop $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/
	cp $(SOURCE)/*.png $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/

.PHONY: all install

