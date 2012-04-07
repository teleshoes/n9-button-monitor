set -x

apt-get install \
  xresponse \
  x11-utils \
  python-qmsystem \
  python-qtmobility.multimediakit \
  python-qtmobility.systeminfo \
  python-pyside.qtgui \
  python-pyside.qtcore \
;

INSTALL_DIR=/opt/n9-button-monitor
UPSTART_DIR=/etc/init/apps
CONF_DIR=/home/user/.config

mkdir -p $INSTALL_DIR
cp n9-button-monitor.py $INSTALL_DIR
chmod +x $INSTALL_DIR/n9-button-monitor.py

cp n9-button-monitor.conf $UPSTART_DIR

mv $CONF_DIR/n9-button-monitor.conf $CONF_DIR/home/user/.config/n9-button-monitor.ini
if [ ! -e $CONF_DIR/n9-button-monitor.ini ]; then
  cp n9-button-monitor.ini $CONF_DIR
fi

