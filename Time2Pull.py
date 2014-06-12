#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This application monitor git repository and warn you when changes have been
made upstream. Basically, it lets you know when one of you colleagure pushed
to the main repository.

The application starts in the system tray. Right clicking on the icon brings
a context menu that let you add new repositories and show the main window.

"""
import sys
from PyQt5 import QtWidgets
from time2pull.window import MainWindow
from time2pull.settings import Settings


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    if not Settings().hide_on_startup:
        win.show()
    app.exec_()
