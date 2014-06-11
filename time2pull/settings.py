"""
Contains the application settings
"""
from PyQt5 import QtCore


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
