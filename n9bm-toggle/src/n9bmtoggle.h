#ifndef N9BMTOGGLE_H
#define N9BMTOGGLE_H

#include "mtabstracttoggle.h"
#include <QtPlugin>
#include <QDebug>

class N9BMToggle : public QObject, public MTAbstractToggle
{
    Q_OBJECT
    Q_INTERFACES(MTAbstractToggle)
public:
    static const QString N9BM_BIN;

    N9BMToggle(QObject *parent = NULL);
    bool isToggle() { return true; }

    QString toggleName() { return "N9 Button Monitor Toggle"; }
    QString toggleDeveloper() { return "Elliot Wolk"; }
    QUrl toggleSupportUrl() { return QUrl("mailto:elliot.wolk@gmail.com"); }
    QImage toggleIcon() { return QImage(); }
    QString toggleIconId() { return "icon-m-bluetooth-carkit"; }

    bool isActive();

private:
    bool m_isActive;

public slots:
    void onToggleClicked();

signals:
    void stateChanged(bool state);
    void iconChanged(QImage icon);
    void iconChanged(QString iconId);
    void isWorkingStateChanged(bool working);
};

#endif // N9BMTOGGLE_H
