#include "n9bmtoggle.h"
#include <QProcess>
#include <qapplication.h>

const QString N9BMToggle::N9BM_BIN =
  QString("/opt/n9-button-monitor/bin/n9-button-monitor.py");

N9BMToggle::N9BMToggle(QObject *parent) :
    QObject(parent)
{
  qApp->installEventFilter(this);
}

int N9BMToggle::run(QString cmd, QStringList args, bool wait)
{
    QProcess p;
    if(wait)
      p.start(cmd, args);
    else
      p.startDetached(cmd, args);

    if(!wait || !p.waitForFinished())
      return -1;
    else
      return p.exitCode();
}

int N9BMToggle::killSignal(QString sig)
{
    return run("pkill", QStringList()
      << ("-" + sig) << "-f" << ("/usr/bin/python " + N9BM_BIN), true);
}

bool N9BMToggle::isActive()
{
    return 0 == killSignal("0");
}

bool N9BMToggle::eventFilter(QObject *obj, QEvent *event)
{
    if (event->type() == QEvent::ApplicationActivate)
        emit onApplicationActivate();
    return QObject::eventFilter(obj, event);
}

void N9BMToggle::onToggleClicked()
{
    bool active = !isActive();
    killSignal("SIGTERM");
    if(active)
        run(N9BM_BIN, QStringList(), false);
    emit stateChanged(active);
}

void N9BMToggle::onApplicationActivate()
{
}

Q_EXPORT_PLUGIN2(n9bmtoggle, N9BMToggle)
