#include "n9bmtoggle.h"

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
    emit stateChanged(m_isActive);
}

Q_EXPORT_PLUGIN2(n9bmtoggle, N9BMToggle)
