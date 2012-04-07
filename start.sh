#!/bin/sh
u=`/usr/bin/whoami`
if [ "$u" != "root" ]; then
  echo must be run as root
  exit 1
fi

sh /opt/n9-button-monitor/stop.sh
/bin/develsh -c "
  source /etc/profile
  PATH=$PATH:/usr/local/bin
  python /opt/n9-button-monitor/n9-button-monitor.py &
"
