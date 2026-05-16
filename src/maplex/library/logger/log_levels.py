from enum import IntEnum

"""
LogLevel Enum for MapleLogger
"""

class LogLevel(IntEnum):

    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5
    NONE = 6
