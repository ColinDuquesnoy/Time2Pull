# -*- coding: utf-8 -*-
"""
Contains the application constans and enumerations
"""
from enum import IntEnum


class RemoteStatus(IntEnum):
    up_to_date = 0
    behind = 1
    ahead = 2
    diverged = 3


class TrayIconType(IntEnum):
    light = 0
    dark = 1
