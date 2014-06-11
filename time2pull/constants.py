"""
Contains the application constans and enumerations
"""
from enum import Enum


class RemoteStatus(Enum):
    up_to_date = -1
    behind = 0
    ahead = 1
    diverged = 2
