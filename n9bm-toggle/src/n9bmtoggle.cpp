#include "n9bmtoggle.h"
#include <QProcess>

const QString N9BMToggle::N9BM_BIN =
  QString("/opt/n9-button-monitor/bin/n9-button-monitor.py");

N9BMToggle::N9BMToggle(QObject *parent) :
    QObject(parent)
{
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

void N9BMToggle::onToggleClicked()
{
    bool m_isActive = !isActive();
    killSignal("SIGTERM");
    if(m_isActive)
    {
        system(N9BM_BIN.toStdString().c_str() +" &");
    }
    emit stateChanged(m_isActive);
}

Q_EXPORT_PLUGIN2(n9bmtoggle, N9BMToggle)
