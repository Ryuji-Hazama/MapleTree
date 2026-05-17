from datetime import datetime
import inspect
import os
from os import path
import sys
import traceback
from typing import Literal

from .json import MapleJson
from .library.logger import *
from .mapleExceptions import *

class Logger:

    from .library.logger import (
        toLogLevel,
        toLogSize,
        isLogLevel
    )

    LogLevel = LogLevel

    def __init__(
            self,
            func: str | None = None,
            workingDirectory: str | None = None,
            cmdLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None,
            fileLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None,
            maxLogSize: float | None = None,
            fileMode: Literal["append", "overwrite", "daily"] | None = None,
            configFile: str = "config.json",
            encoding: str | None = None,
            timestampFormat: str | None = None,
            **kwargs
        ) -> None:

        """
        Set a negative value to maxLogSize for an infinite log file size.
        """

        try:

            self.consoleColors = getConsoleColors()
            loggerParams = {
                "func": func,
                "workingDirectory": workingDirectory,
                "cmdLogLevel": cmdLogLevel,
                "fileLogLevel": fileLogLevel,
                "maxLogSize": maxLogSize,
                "fileMode": fileMode,
                "configFile": configFile,
                "encoding": encoding,
                "timestampFormat": timestampFormat,
                "getLogger": kwargs.get("getLogger", False),
                "consoleAlignWidth": kwargs.get("consoleAlignWidth", 16),
                "fileAlignWidth": kwargs.get("fileAlignWidth", 4)
            }
            self.config = LoggerConfig(loggerParams)

        except Exception as ex:

            print(f"{self.consoleColors.Red}Error initializing logger: {ex}{self.consoleColors.Reset}")
            raise MapleLoggerException(f"Error initializing logger: {ex}") from ex

    #################################
    # Getters and Setters

    def getLogFile(self) -> str:

        '''Get log file path'''

        return self.config.logfile
    
    def setLogFile(self, logfile: str) -> None:

        '''Set log file path'''

        self.config.logfile = logfile

    def getConsoleLogLevel(self) -> LogLevel:

        '''
        Get console log level
        getConsoleLogLevel() -> LogLevel(int)
        getConsoleLogLevel().name -> str
        '''

        return self.config.consoleLogLevel

    def setConsoleLogLevel(self, loglevel: object) -> None:

        '''Set console log level'''

        try:

            self.config.consoleLogLevel = toLogLevel(loglevel)

        except MapleInvalidLoggerLevelException as ex:

            raise MapleInvalidLoggerLevelException(loglevel, "Invalid console log level. Log level must be a string or integer corresponding to a valid log level.") from ex
        
    def getFileLogLevel(self) -> LogLevel:

        '''
        Get file log level
        getFileLogLevel() -> LogLevel(int)
        getFileLogLevel().name -> str
        '''

        return self.config.fileLogLevel
    
    def setFileLogLevel(self, loglevel: object) -> None:

        '''Set file log level'''

        try:

            self.config.fileLogLevel = toLogLevel(loglevel)

        except MapleInvalidLoggerLevelException as ex:

            raise MapleInvalidLoggerLevelException(loglevel, "Invalid file log level. Log level must be a string or integer corresponding to a valid log level.") from ex
    
    def getMaxLogSize(self) -> float:

        '''Get max log size'''

        return self.config.maxLogSize
        
    def setMaxLogSize(self, maxLogSize: object) -> None:

        '''Set max log size'''

        try:

            self.config.maxLogSize = toLogSize(maxLogSize)

        except MapleLoggerException as ex:

            raise MapleLoggerException("Invalid max log size. Log size must be an integer, float or string.") from ex

    #
    #################################
    # Logger

    def logWriter(self, loglevel: LogLevel, message: object, callerDepth: int = 1) -> None:

        """
        Output log to log file and console.
        """

        # Precheck log level

        if loglevel < self.config.consoleLogLevel and loglevel < self.config.fileLogLevel:

            return

        # Console colors

        Black = self.consoleColors.Black
        bBlack = self.consoleColors.bBlack
        Red = self.consoleColors.Red
        bRed = self.consoleColors.bRed
        Green = self.consoleColors.Green
        bLightBlue = self.consoleColors.bLightBlue
        Bold = self.consoleColors.Bold
        Italic = self.consoleColors.Italic
        Reset = self.consoleColors.Reset

        try:

            # Get caller informations

            callerFrame = inspect.stack()[callerDepth]
            callerFunc = callerFrame.function
            callerLine = callerFrame.lineno

            # Set console color

            match loglevel:

                case self.LogLevel.TRACE:

                    col = bBlack

                case self.LogLevel.DEBUG:

                    col = Green

                case self.LogLevel.INFO:

                    col = bLightBlue

                case self.LogLevel.WARN:

                    col = bRed

                case self.LogLevel.ERROR:

                    col = Red

                case self.LogLevel.FATAL:

                    col = Bold + Red

                case self.LogLevel.NONE:

                    col = Bold + Italic + Black

                case _:

                    col = ""

            # Export to console and log file

            if loglevel >= self.config.consoleLogLevel:
                consolePrefix = f"[{col}{loglevel.name:5}{Reset}]{Green}{self.config.func}{Reset} {bBlack}{callerFunc}({callerLine}){Reset}"
                colorLength = len(col) + len(Reset) + len(Green) + len(Reset) + len(bBlack) + len(Reset)
                consolePrefixLength = len(consolePrefix) - colorLength
                consoleAlignWidth = self.config.consoleAlignWidth * (consolePrefixLength // self.config.consoleAlignWidth + (1 if consolePrefixLength % self.config.consoleAlignWidth != 0 else 0))
                consoleAlignWidth += colorLength
                print(f"{consolePrefix:<{consoleAlignWidth}}: {message}")
        
            if loglevel >= self.config.fileLogLevel:

                timeStamp = datetime.now().strftime(self.config.timestampFormat)[:-3]
                prefixString = f"({self.config.pid}) {timeStamp} [{loglevel.name:5}]{self.config.func} {self.config.callerName}{callerFunc}({callerLine})"
                prefixLength = len(prefixString)
                alignWidth = self.config.fileAlignWidth * (prefixLength // self.config.fileAlignWidth + (1 if prefixLength % self.config.fileAlignWidth != 0 else 0))

                for i in range(3):

                    try:

                        with open(self.config.logfile, "a", encoding=self.config.encoding) as f:
                            print(f"{prefixString:<{alignWidth}}: {message}", file=f)

                        break

                    except IOError:

                        if i == 2:
                            raise

        except Exception as ex:

            raise MapleLoggerException(f"Failed to write log: {ex}") from ex

        if self.config.maxLogSize > 0:

            # Check file size

            try:

                if path.exists(self.config.logfile) and path.getsize(self.config.logfile) > self.config.maxLogSize:

                    # Rename log file

                    if self.config.fileMode == "overwrite":

                        if path.isfile(f"{self.config.logfile}_old.log"):

                            os.remove(f"{self.config.logfile}_old.log")

                        os.rename(self.config.logfile, f"{self.config.logfile}_old.log")
                        return

                    elif self.config.fileMode == "daily":

                        dateStr = ""

                    else:

                        dateStr = f"_{datetime.now():%Y%m%d_%H%M%S}"
                    
                    i = 0
                    logCopyFile = f"{self.config.logfile}{dateStr}{i}.log"

                    while path.isfile(logCopyFile):

                        i += 1
                        logCopyFile = f"{self.config.logfile}{dateStr}{i}.log"

                    os.rename(self.config.logfile, logCopyFile)

            except Exception as ex:

                raise MapleLoggerException(f"Failed to rotate log file: {ex}") from ex

    #
    ################################
    # Trace

    def trace(self, object: any):

        '''Trace log'''

        self.logWriter(self.LogLevel.TRACE, object, callerDepth=2)
    #
    ################################
    # Debug

    def debug(self, object: any):

        '''Debug log'''

        self.logWriter(self.LogLevel.DEBUG, object, callerDepth=2)

    #
    ################################
    # Info

    def info(self, object: any):

        '''Info log'''

        self.logWriter(self.LogLevel.INFO, object, callerDepth=2)

    #
    ################################
    # Warn

    def warn(self, object: any):

        '''Warn log'''

        self.logWriter(self.LogLevel.WARN, object, callerDepth=2)

    #
    ################################
    # Error

    def error(self, object: any):

        '''Error log'''

        self.logWriter(self.LogLevel.ERROR, object, callerDepth=2)

    #
    ################################
    # Fatal

    def fatal(self, object: any):

        '''Fatal log'''

        self.logWriter(self.LogLevel.FATAL, object, callerDepth=2)

    #
    ################################
    # None

    def log(self, object: any):

        '''None log'''

        self.logWriter(self.LogLevel.NONE, object, callerDepth=2)

    #
    ################################
    # Error messages

    def ShowError(self, ex: Exception, message: str | None = None, fatal: bool = False):

        '''Show and log error'''

        if fatal:

            logLevel = self.LogLevel.FATAL

        else:

            logLevel = self.LogLevel.ERROR

        if message is not None:

            self.logWriter(logLevel, message, callerDepth=2)

        self.logWriter(logLevel, f"{ex}\n{traceback.format_exc()}", callerDepth=2)

    #
    ################################
    # Save log settings to config file

    def saveLogSettings(self) -> None:

        '''Save current log settings to config file'''

        try:

            self.config.saveLogSettings(self.config.logConfInstance)

        except Exception as ex:

            print(f"{self.consoleColors.Red}Warning: Failed to save log settings to config file: {ex}{self.consoleColors.Reset}")

# Dictionary to hold Logger instances

_loggers: dict[str, Logger] = {}

# Get or create a Logger instance

def getLogger(name: str = "", **kwargs) -> Logger:
    """
    Get or create a Logger instance.
    
    Args:
        name: Logger name (usually __name__ of the calling module)
        **kwargs: Arguments to pass to Logger constructor if creating new instance
    
    Returns:
        Logger instance
    """

    if name not in _loggers:
        kwargs["getLogger"] = True
        _loggers[name] = Logger(func=name, **kwargs)

    return _loggers[name]

def getDailyLogger(name: str = "", **kwargs) -> Logger:
    """
    Get or create a daily Logger instance.
    
    Args:
        name: Logger name (usually __name__ of the calling module)
        **kwargs: Arguments to pass to Logger constructor if creating new instance
    
    Returns:
        Logger instance
    """

    if name not in _loggers:
        kwargs["getLogger"] = True
        _loggers[name] = Logger(func=name, fileMode="daily", **kwargs)

    return _loggers[name]

""" * * * * * * * * * * * * * """
"""
ToDo list:

* Logger *

- Add option to set date format
- Add set* functions
- Configure log format in config file

"""
""" * * * * * * * * * * * * * """
