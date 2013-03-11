#include "n9bmtoggle.h"

const QString N9BMToggle::N9BM_BIN =
  QString("/opt/n9-button-monitor/bin/n9-button-monitor.py");

N9BMToggle::N9BMToggle(QObject *parent) :
    QObject(parent),
    m_isActive(false)
{
}

bool N9BMToggle::isActive()
{
    return m_isActive;
}

void N9BMToggle::onToggleClicked()
{
    m_isActive = !m_isActive;
    system("pkill -f " + N9BM_BIN.toStdString().c_str());
    if(m_isActive)
    {
        system(N9BM_BIN.toStdString().c_str() +" &");
    }
    emit stateChanged(m_isActive);
}

Q_EXPORT_PLUGIN2(n9bmtoggle, N9BMToggle)
