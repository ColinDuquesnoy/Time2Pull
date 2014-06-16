import sys
from PyQt5 import QtWidgets
from time2pull.window import MainWindow
from time2pull.settings import Settings


def main():
    global app, win
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    if not Settings().hide_on_startup:
        win.show()
    app.exec_()

