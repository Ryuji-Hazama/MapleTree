import sys

from .log_levels import LogLevel
from src.maplex.mapleColors import ConsoleColors
from src.maplex.mapleExceptions import *

########################
# Console colors for cross-platform compatibility

def getConsoleColors() -> ConsoleColors:

    '''Get console colors instance'''

    if hasattr(sys, "getwindowsversion") and sys.getwindowsversion().build < 22000:

        consoleColors = ConsoleColors(Black="", Red="", Green="", Yellow="", Blue="", Magenta="", LightBlue="", White="",
                                        bgBlack="", bgRed="", bgGreen="", bgYellow="", bgBlue="", bgMagenta="", bgLightBlue="", bgWhite="",
                                        bBlack="", bRed="", bGreen="", bYellow="", bBlue="", bMagenta="", bLightBlue="", bWhite="",
                                        Bold="", Underline="", Reversed="", Reset="")

    else:

        consoleColors = ConsoleColors()

    return consoleColors

#
####################
# Convert to log level

def toLogLevel(loglevel: any) -> LogLevel:

    '''Convert object to log level'''

    if type(loglevel) is str:

        loglevelClass = isLogLevel(loglevel)

        if loglevelClass == -1:

            raise MapleInvalidLoggerLevelException(loglevel, f"Invalid logger level string")

    elif type(loglevel) is int:

        if loglevel < 0 or loglevel > len(LogLevel) - 1:

            raise MapleInvalidLoggerLevelException(loglevel, f"Invalid logger level value")
            
        else:

            loglevelClass = LogLevel(loglevel)

    elif type(loglevel) is not LogLevel:

        raise MapleInvalidLoggerLevelException(loglevel,f"Invalid logger level type: {type(loglevel)}")

    else:

        loglevelClass = loglevel

    return loglevelClass

#
######################
# Convert log size

def toLogSize(logSize: any) -> int:

    '''Convert log size to bytes'''

    if type(logSize) in {int, float}:

        return int(logSize * 1000000)

    elif type(logSize) is str:

        if logSize.lower().endswith("m"):

            return int(float(logSize[:-1]) * 1000000)

        elif logSize.lower().endswith("g"):

            return int(float(logSize[:-1]) * 1000000000)

        else:

            return int(float(logSize) * 1000000)
    
    else:

        raise MapleLoggerException(f"Invalid log size type: {type(logSize)}. Log size must be an integer, float or string.")

#
################
# Check log level

def isLogLevel(lLStr: str) -> LogLevel:

    '''Check if string is a valid log level'''

    logLevelStr = lLStr.upper()

    for lLevel in LogLevel:
        if logLevelStr == lLevel.name:
            return lLevel

    return -1
