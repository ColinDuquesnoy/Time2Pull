"""
Contains the application settings
"""
from PyQt5 import QtCore
import sys
from time2pull.constants import TrayIconType

class Settings:
    def __init__(self):
        self._settings = QtCore.QSettings('Time2Pull')

    @property
    def repositories(self):
        ret_val = self._settings.value('repositories', '')
        if not ret_val:
            ret_val = []
        elif isinstance(ret_val, str):
            ret_val = [ret_val]
        return ret_val

    @repositories.setter
    def repositories(self, value):
        self._settings.setValue('repositories', value)

    @property
    def tray_icon_type(self):
        default = (TrayIconType.dark if sys.platform == 'darwin'
                   else TrayIconType.light)
        return TrayIconType(self._settings.value('tray_icon_type', int(default)))

    @tray_icon_type.setter
    def tray_icon_type(self, value):
        self._settings.setValue('tray_icon_type', int(value))