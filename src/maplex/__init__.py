"""
MapleTree: A Python library for building and managing hierarchical data structures with ease.
Logger: A simple logging utility for tracking events and debugging.
"""

from .mapleColors import ConsoleColors
from .mapleJson import MapleJson
from .mapleLogger import Logger, getLogger
from .mapleExceptions import (
    InvalidMapleFileFormatException,
    KeyEmptyException,
    MapleDataNotFoundException,
    MapleException,
    MapleEncryptionNotEnabledException,
    MapleFileEmptyException,
    MapleFileLockedException,
    MapleFileNotFoundException,
    MapleHeaderNotFoundException,
    MapleSyntaxException,
    MapleTagNotFoundException,
    MapleTypeException,
    NotAMapleFileException
)
from .mapleTreeEditor import MapleTree
from .utils import winHide, winUnHide

__all__ = [
    'ConsoleColors',
    'getLogger',
    'InvalidMapleFileFormatException',
    'KeyEmptyException',
    'MapleDataNotFoundException',
    'MapleEncryptionNotEnabledException',
    'MapleException',
    'MapleFileEmptyException',
    'MapleFileLockedException',
    'MapleFileNotFoundException',
    'MapleHeaderNotFoundException',
    'MapleJson',
    'MapleSyntaxException',
    'MapleTagNotFoundException',
    'MapleTypeException',
    'NotAMapleFileException',
    'MapleTree',
    'Logger',
    'winHide',
    'winUnHide'
]

__version__ = "3.0.0.dev2"
__author__ = "Ryuji Hazama"
__license__ = "MIT"