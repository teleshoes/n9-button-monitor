#include "n9bmtoggle.h"

PSMToggle::PSMToggle(QObject *parent) :
    QObject(parent),
    m_deviceMode(new MeeGo::QmDeviceMode(this)),
    m_isWorking(false)
{
    connect(m_deviceMode, SIGNAL(devicePSMStateChanged(MeeGo::QmDeviceMode::PSMState)),
            this, SLOT(onPSMStateChanged(MeeGo::QmDeviceMode::PSMState)));
}

bool PSMToggle::getIsPSMModeFromPSMState(MeeGo::QmDeviceMode::PSMState mode)
{
    bool isPSMMode = false;
    switch (mode) {
    case MeeGo::QmDeviceMode::PSMStateOff:
        isPSMMode = false;
        break;
    case MeeGo::QmDeviceMode::PSMStateOn:
        isPSMMode = true;
        break;
    case MeeGo::QmDeviceMode::PSMError:
        isPSMMode = false;
        break;
    }

    return isPSMMode;
}

bool PSMToggle::isActive()
{
    MeeGo::QmDeviceMode::PSMState mode = m_deviceMode->getPSMState();
    return getIsPSMModeFromPSMState(mode);
}

void PSMToggle::onToggleClicked()
{
    m_isWorking = true;
    emit isWorkingStateChanged(m_isWorking);

    if (isActive())
        m_deviceMode->setPSMState(MeeGo::QmDeviceMode::PSMStateOff);
    else
        m_deviceMode->setPSMState(MeeGo::QmDeviceMode::PSMStateOn);

    m_isWorking = false;
    emit isWorkingStateChanged(m_isWorking);
}

void PSMToggle::onPSMStateChanged(MeeGo::QmDeviceMode::PSMState state)
{
    bool isPSMMode = getIsPSMModeFromPSMState(state);
    m_isActive = isPSMMode;
    emit stateChanged(m_isActive);
}

Q_EXPORT_PLUGIN2(psmtoggle, PSMToggle)
