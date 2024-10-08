"""Module "keyboards".

File:
    __init__.py

About:
    Initializing the "keyboards" module
"""

from .color import ButtonColor
from .keyboard import Keyboard
from .action import Text, OpenLink, OpenApp, Location, VKPay, Callback
from .answer import SnackbarAnswer, AppAnswer, LinkAnswer


__all__ = (
    "ButtonColor",
    "Keyboard",
    "Text",
    "OpenLink",
    "OpenApp",
    "Location",
    "VKPay",
    "Callback",
    "SnackbarAnswer",
    "AppAnswer",
    "LinkAnswer",
)
