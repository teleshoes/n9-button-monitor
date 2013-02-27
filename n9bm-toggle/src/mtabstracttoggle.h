/* Copyright 2012 Mohammad Abu-Garbeyyeh
 * This file is part of mt-toggles.
 * It is licensed under the GPLv2.
 */
#ifndef MTABSTRACTTOGGLE_H
#define MTABSTRACTTOGGLE_H

#include <QString>
#include <QUrl>
#include <QtGui/QImage>

class MTAbstractToggle
{
public:
    /* isToggle() should returns whether this is a toggle or not, not being
     * a toggle means that the widget created should not have a visual switch
     * and that the toggle would only act as a button */
    virtual bool isToggle() = 0;

    /* isActive() should return the current state of the widget, whatever it
     * returns should be the same as the state indicated by the signal
     * void toggleStateChanged(bool state) */
    virtual bool isActive() = 0;

    /* toggleName() should return the name of the plugin/toggle, for example
     * a WiFi toggle would return "WiFi Toggle" or "WiFi" */
    virtual QString toggleName() = 0;

    /* toggleDeveloper() should return the name of the developer of the toggle,
     * this may not be used at first, but it may help in support cases */
    virtual QString toggleDeveloper() = 0;

    /* toggleSupportUrl() should return the URL to contact in case there's a
     * problem with the toggle, this can be a null QUrl. */
    virtual QUrl toggleSupportUrl() = 0;

    /* toggleIcon() should return the icon to be shown in the toggle's widget,
     * in case this icon needs to be dynamic, it can be changed by emitting
     * iconChanged(QImage icon). */
    virtual QImage toggleIcon() = 0;

    /* toggleIconId() should return the ID of the image to be used in case
     * the method toggleIcon() returns a null image, if both this and the above
     * are null, the plugin will not be loaded. It can similarly be changed
     * by emitting iconChanged(QString iconId). */
    virtual QString toggleIconId() = 0;

    /* Due to limitations in Qt's Plugin interface, I can't provide virtual slots
     * since this class doesn't inherit QObject, please define these in your plugin.

signals:
    void stateChanged(bool state);
    void isWorkingStateChanged(bool working);

    // Define both signals, you can use only one if you want depending on what
    // method you used to provide the icon.
    void iconChanged(QImage icon);
    void iconChanged(QString iconId);

public slots:
    void onToggleClicked();
    */
};

Q_DECLARE_INTERFACE(MTAbstractToggle, "org.xceleo.mohammadag.MTAbstractToggle/1.0")

#endif // MTABSTRACTTOGGLE_H
