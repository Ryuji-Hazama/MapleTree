"""
Split mapleLogger.py into multiple files for better organization and maintainability.
"""

from .config import LoggerConfig
from .log_levels import LogLevel
from .utilities import *

__all__ = [
    "LoggerConfig",
    "LogLevel",
    "getConsoleColors",
    "toLogLevel",
    "toLogSize",
    "isLogLevel"
]