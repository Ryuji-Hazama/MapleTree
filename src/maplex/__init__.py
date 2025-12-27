"""
MapleTree: A Python library for building and managing hierarchical data structures with ease.
Logger: A simple logging utility for tracking events and debugging.
"""

from .mapleColors import ConsoleColors
from .mapleLogger import Logger
from .mapleExceptions import (
    InvalidMapleFileFormatException,
    KeyEmptyException,
    MapleDataNotFoundException,
    MapleException,
    MapleFileEmptyException,
    MapleFileLockedException,
    MapleFileNotFoundException,
    MapleHeaderNotFoundException,
    MapleTagNotFoundException,
    NotAMapleFileException
)
from .mapleTreeEditor import MapleTree
from .utils import winHide, winUnHide

__all__ = [
    'ConsoleColors',
    'InvalidMapleFileFormatException',
    'KeyEmptyException',
    'MapleDataNotFoundException',
    'MapleException',
    'MapleFileEmptyException',
    'MapleFileLockedException',
    'MapleFileNotFoundException',
    'MapleHeaderNotFoundException',
    'MapleTagNotFoundException',
    'NotAMapleFileException',
    'MapleTree',
    'Logger',
    'winHide',
    'winUnHide'
]

__version__ = "2.0.0"
__author__ = "Ryuji Hazama"
__license__ = "MIT"