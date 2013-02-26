install(
  FILES
    n9-button-monitor.conf
  DESTINATION
    /etc/init/apps
)

install(
  FILES
    n9-button-monitor.desktop
  DESTINATION
    /usr/share/applications
)

install(
  FILES
    startstop.sh
    off.desktop
    on.desktop
  DESTINATION
    /opt/n9-button-monitor/bin
)

install(
  FILES
    n9bm-on.png
    n9bm-off.png
  DESTINATION
    /usr/share/icons/hicolor/80x80/apps
)
