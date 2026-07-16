"""
Logger: A simple logging utility for tracking events and debugging.
MapleJson: A utility for handling JSON data with enhanced features.
ConsoleColors: A collection of ANSI escape codes for colored console output.
MapleTree: A Python library for building and managing hierarchical data structures with ease.
MapleExceptions: A set of custom exceptions for handling specific error cases in the MapleX library.
"""

from .mapleColors import ConsoleColors
from .jsonHandler import MapleJson, getMapleJson
from .mapleLogger import Logger, getLogger, getDailyLogger
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
    'getDailyLogger',
    'getMapleJson',
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

__version__ = "3.1.2"
__author__ = "Ryuji Hazama"
__license__ = "MIT"


""" * * * * * * * * * * * * * """
"""
ToDo list:

* MapleX *

- Restructure MapleX to be more modular and maintainable

"""
""" * * * * * * * * * * * * * """
