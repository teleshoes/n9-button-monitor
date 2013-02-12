install(
  FILES
    n9-button-monitor.conf
  DESTINATION
    /etc/init/apps
)

install(
  FILES
    n9bm-toggle.desktop
    n9bm-gui.desktop
  DESTINATION
    /usr/share/applications
)

install(
  FILES
    startstop.sh
  DESTINATION
    /opt/n9-button-monitor
)

install(
  FILES
    n9bm-on.png
    n9bm-off.png
  DESTINATION
    /usr/share/icons/hicolor/80x80/apps
)
