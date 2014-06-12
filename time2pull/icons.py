# -*- coding: utf-8 -*-
"""
This module helps manage overlayed icons.
"""
from PyQt5 import QtCore, QtGui
from time2pull.constants import RemoteStatus, TrayIconType
from time2pull.settings import Settings


def get_status_icon(has_local_changes=False, status=RemoteStatus.up_to_date,
             size=QtCore.QSize(64, 64), offset=(0, 0)):
    base = ':/time2pull/icons/Database.png' if not has_local_changes else \
        ':/time2pull/icons/DatabaseDirty.png'
    icons = {
        RemoteStatus.up_to_date: None,
        RemoteStatus.behind: ':/time2pull/icons/Download.png',
        RemoteStatus.ahead: ':/time2pull/icons/Upload.png',
        RemoteStatus.diverged: ':/time2pull/icons/DownloadUpload.png'
    }
    overlay_icon = QtGui.QIcon(icons[status])
    if overlay_icon:
        icon_pixmap = QtGui.QIcon(base).pixmap(size)
        painter = QtGui.QPainter(icon_pixmap)
        painter.drawPixmap(offset[0], offset[1], overlay_icon.pixmap(48, 48))
        painter.end()
        return QtGui.QIcon(icon_pixmap)
    else:
        return QtGui.QIcon(base)


def get_tray_icon(is_behind):
    if is_behind:
        return QtGui.QIcon(':/time2pull/icons/Download.png')
    else:
        icons = {
            TrayIconType.light: ':/time2pull/icons/Download-light.png',
            TrayIconType.dark: ':/time2pull/icons/Download-dark.png'
        }
        return QtGui.QIcon(icons[Settings().tray_icon_type])


if __name__ == '__main__':
    # example: show all possible combination in an example list
    from PyQt5 import QtWidgets
    import sys
    from time2pull.forms import resources_rc

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QListWidget()
    window.setIconSize(QtCore.QSize(64, 64))
    window.resize(640, 480)
    for dirty, prefix in zip([False, True], ['No un-committed changes', 'Un-committed changes']):
        for status in RemoteStatus:
            item = QtWidgets.QListWidgetItem()
            item.setIcon(get_status_icon(dirty, status))
            item.setText('%s - %s' % (prefix, str(status)))
            window.addItem(item)
    window.setWindowIcon(get_tray_icon(True))
    window.show()
    app.exec_()
