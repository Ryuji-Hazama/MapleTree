"""
Split mapleLogger.py into multiple files for better organization and maintainability.
"""

from .config import LoggerConfig
from .file_handler import FileHandler
from .formatter import Formatter
from .log_levels import LogLevel
from .utilities import *

__all__ = [
    "FileHandler",
    "Formatter",
    "LoggerConfig",
    "LogLevel",
    "getConsoleColors",
    "toLogLevel",
    "toLogSize",
    "isLogLevel"
]