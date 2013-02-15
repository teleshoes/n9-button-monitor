
# Ye Olde Camerra Hack (http://thp.io/2012/camerra/)
# Copyright (c) 2012 Thomas Perl <thp.io/about>

APP_NAME = adv-button-monitor

all:
	true

install:
	mkdir -p $(DESTDIR)/opt/$(APP_NAME)/
	cp *.sh *.py $(DESTDIR)/opt/$(APP_NAME)/
	cp off.desktop $(DESTDIR)/opt/$(APP_NAME)/
	cp on.desktop $(DESTDIR)/opt/$(APP_NAME)/
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp $(APP_NAME).desktop $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/
	cp *.png $(DESTDIR)/usr/share/icons/hicolor/80x80/apps/

.PHONY: all install

