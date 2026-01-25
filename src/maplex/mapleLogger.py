from datetime import datetime
import inspect
import os
from os import path
import sys
import traceback
from enum import IntEnum
from typing import Literal
from .mapleJson import MapleJson
from .mapleColors import ConsoleColors
from .mapleExceptions import *

class Logger:

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
            **kwargs
        ) -> None:

        """
        Set a negative value to maxLogSize for an infinite log file size.
        """

        self.intMaxValue = 4294967295
        self.consoleLogLevel = -1
        self.fileLogLevel = -1
        self.CWD = os.getcwd()
        self.pid = os.getpid()
        self.consoleColors = ConsoleColors()
        self.fileMode = "append" if fileMode is None else fileMode
        self.encoding = encoding

        # Check the OS (Windows 10 or older cannot change the console color)

        if hasattr(sys, "getwindowsversion") and sys.getwindowsversion().build < 22000:

            self.consoleColors = ConsoleColors(Black="", Red="", Green="", Yellow="", Blue="", Magenta="", LightBlue="", White="",
                                            bgBlack="", bgRed="", bgGreen="", bgYellow="", bgBlue="", bgMagenta="", bgLightBlue="", bgWhite="",
                                            bBlack="", bRed="", bGreen="", bYellow="", bBlue="", bMagenta="", bLightBlue="", bWhite="",
                                            Bold="", Underline="", Reversed="", Reset="")

        #
        ############################
        # Check config file

        self.CONFIG_KEY = "MapleLogger"
        self.CONSOLE_LOG_LEVEL = "ConsoleLogLevel"
        self.FILE_LOG_LEVEL = "FileLogLevel"
        self.MAX_LOG_SIZE = "MaxLogSize"
        self.WORKING_DIRECTORY = "WorkingDirectory"
        self.FILE_ENCODING = "FileEncoding"

        # Set config file path
        
        if path.isabs(configFile):

            self.configFile = configFile

        else:

            self.configFile = path.join(self.CWD, configFile)

        # Try to read config file

        try:

            logConfInstance = MapleJson(self.configFile)

            if path.isfile(self.configFile):

                confJson = logConfInstance.read()

            else:

                confJson = {}

        except Exception as ex:

            print(f"{self.consoleColors.Red}Warning: Failed to read logger config file: {ex}{self.consoleColors.Reset}")
            confJson = {}
            logConfInstance = None

        # Read configuration

        logConf = confJson.get(self.CONFIG_KEY, None)

        if logConf is None:

            logConf = {}
            logConf[self.CONSOLE_LOG_LEVEL] = "INFO"
            logConf[self.FILE_LOG_LEVEL] = "INFO"
            logConf[self.MAX_LOG_SIZE] = 3
            logConf[self.WORKING_DIRECTORY] = "logs"

        #
        ############################
        # Check output directory
        
        if workingDirectory is not None:

            self.CWD = workingDirectory

        else:

            self.CWD = logConf.get(self.WORKING_DIRECTORY, None)

        if self.CWD in {"", None}:

            self.CWD = path.join(os.getcwd(), "logs")
            logConf[self.WORKING_DIRECTORY] = self.CWD

        elif not path.isabs(self.CWD):

            self.CWD = path.join(os.getcwd(), self.CWD)

        #############################
        # Set log file name

        if fileMode == "daily":

            self.logfile = path.join(self.CWD, f"log_{datetime.now():%Y%m%d}.log")
        
        else:

            self.logfile = path.join(self.CWD, "AppLog.log")

        #
        ############################
        # Check log directory

        if not path.isdir(path.join(self.CWD)):
            os.makedirs(path.join(self.CWD))

        #
        ############################
        # Set function name

        isGetLogger = kwargs.get("getLogger", False)

        if isGetLogger:

            caller = inspect.currentframe().f_back.f_back.f_globals.get("__name__", "")

        else:

            caller = inspect.currentframe().f_back.f_globals.get("__name__", "")

        if func in {None, ""}:

            self.func = ""
            self.callerName = ""
        
        elif func != caller:

            self.func = f"[{func}]"
            self.callerName = ""

        else:

            self.func = ""
            self.callerName = f"{caller}."

        #
        ############################
        # Set max log file size

        self.maxLogSize = 0

        if maxLogSize is not None:

            self.setMaxLogSize(maxLogSize)

        else:

            try:

                logSize = logConf.get(self.MAX_LOG_SIZE, None)

                if logSize is not None:

                    self.setMaxLogSize(logSize)

                else:

                    self.maxLogSize = 3000000
                    logConf[self.MAX_LOG_SIZE] = 3

            except MapleLoggerException as ex:

                print(f"{self.consoleColors.Red}Warning: Invalid MaxLogSize value provided. Using default value.{self.consoleColors.Reset}")
                self.maxLogSize = 3000000

        if self.maxLogSize == 0:

            print(f"{self.consoleColors.Red}Warning: Infinite log file size is not recommended. Using default value.{self.consoleColors.Reset}")
            self.maxLogSize = 3000000

        #
        ############################
        # Set output log levels

        self.consoleLogLevel = -1
        self.fileLogLevel = -1

        # Console log level

        if cmdLogLevel is not None:

            consoleLogLevel = cmdLogLevel

        else:

            consoleLogLevel = logConf.get(self.CONSOLE_LOG_LEVEL, None)

            if consoleLogLevel is None:

                consoleLogLevel = "INFO"
                logConf[self.CONSOLE_LOG_LEVEL] = consoleLogLevel

        try:

            self.consoleLogLevel = self.toLogLevel(consoleLogLevel)

        except MapleInvalidLoggerLevelException as ex:

            print(f"{self.consoleColors.Red}Warning: Invalid console log level provided: [{consoleLogLevel}]. Using default value.{self.consoleColors.Reset}")
            self.consoleLogLevel = self.LogLevel.INFO

        # File log level

        if fileLogLevel is not None:

            self.fileLogLevel = self.isLogLevel(fileLogLevel)

        else:

            fileLogLevel = logConf.get(self.FILE_LOG_LEVEL, None)

            if fileLogLevel is None:

                fileLogLevel = "INFO"
                logConf[self.FILE_LOG_LEVEL] = fileLogLevel

        try:
            
            self.fileLogLevel = self.toLogLevel(fileLogLevel)

        except MapleInvalidLoggerLevelException as ex:

            print(f"{self.consoleColors.Red}Warning: Invalid file log level provided: [{fileLogLevel}]. Using default value.{self.consoleColors.Reset}")
            self.fileLogLevel = self.LogLevel.INFO

        #
        ############################
        # Set file encoding

        if encoding is not None:

            self.encoding = encoding

        else:

            fileEncoding = logConf.get(self.FILE_ENCODING, None)

            if fileEncoding is None:

                fileEncoding = "utf-8"
                logConf[self.FILE_ENCODING] = fileEncoding

            self.encoding = fileEncoding

        # Save config file

        if logConfInstance is not None:

            try:

                confJson[self.CONFIG_KEY] = logConf
                logConfInstance.write(confJson)

            except Exception as ex:

                print(f"{self.consoleColors.Red}Warning: Failed to write logger config file: {ex}{self.consoleColors.Reset}")
        
    #
    #####################
    # Set log level enum

    class LogLevel(IntEnum):

        TRACE = 0
        DEBUG = 1
        INFO = 2
        WARN = 3
        ERROR = 4
        FATAL = 5
        NONE = 6

    #
    #####################
    # Getters and Setters

    def getLogFile(self) -> str:

        '''Get log file path'''

        return self.logfile
    
    def setLogFile(self, logfile: str) -> None:

        '''Set log file path'''

        self.logfile = logfile

    def getConsoleLogLevel(self) -> LogLevel:

        '''
        Get console log level
        getConsoleLogLevel() -> LogLevel(int)
        getConsoleLogLevel().name -> str
        '''

        return self.consoleLogLevel

    def setConsoleLogLevel(self, loglevel: any) -> None:

        '''Set console log level'''

        try:

            self.consoleLogLevel = self.toLogLevel(loglevel)

        except MapleInvalidLoggerLevelException as ex:

            raise MapleInvalidLoggerLevelException(loglevel, "Invalid console log level. Log level must be a string or integer corresponding to a valid log level.") from ex
        
    def getFileLogLevel(self) -> LogLevel:

        '''
        Get file log level
        getFileLogLevel() -> LogLevel(int)
        getFileLogLevel().name -> str
        '''

        return self.fileLogLevel
    
    def setFileLogLevel(self, loglevel: any) -> None:

        '''Set file log level'''

        try:

            self.fileLogLevel = self.toLogLevel(loglevel)

        except MapleInvalidLoggerLevelException as ex:

            raise MapleInvalidLoggerLevelException(loglevel, "Invalid file log level. Log level must be a string or integer corresponding to a valid log level.") from ex
    
    def getMaxLogSize(self) -> float:

        '''Get max log size'''

        return self.maxLogSize
        
    def setMaxLogSize(self, maxLogSize: any) -> None:

        '''Set max log size'''

        try:

            self.maxLogSize = self.toLogSize(maxLogSize)

        except MapleLoggerException as ex:

            raise MapleLoggerException("Invalid max log size. Log size must be an integer, float or string.") from ex

    #
    ######################
    # Convert log size

    def toLogSize(self, logSize: any) -> int:

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
    ####################
    # Convert to log level

    def toLogLevel(self, loglevel: any) -> LogLevel:

        '''Convert to log level'''

        if type(loglevel) is str:

            loglevelClass = self.isLogLevel(loglevel)

            if loglevelClass == -1:

                raise MapleInvalidLoggerLevelException(loglevel, f"Invalid logger level string")

        elif type(loglevel) is int:

            if loglevel < 0 or loglevel > len(self.LogLevel) - 1:

                raise MapleInvalidLoggerLevelException(loglevel, f"Invalid logger level value")
                
            else:

                loglevelClass = self.LogLevel(loglevel)

        elif type(loglevel) is not self.LogLevel:

            raise MapleInvalidLoggerLevelException(loglevel,f"Invalid logger level type: {type(loglevel)}")

        else:

            loglevelClass = loglevel

        return loglevelClass

    #
    ################
    # Check log level

    def isLogLevel(self, lLStr: str) -> LogLevel:

        for lLevel in self.LogLevel:
            if lLStr == lLevel.name:
                return lLevel

        return -1

    #
    #################################
    # Logger

    def logWriter(self, loglevel: LogLevel, message: any, callerDepth: int = 1) -> None:

        """
        Output log to log file and console.
        """

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

            if loglevel >= self.consoleLogLevel:
                print(f"[{col}{loglevel.name:5}{Reset}]{Green}{self.func}{Reset} {bBlack}{callerFunc}({callerLine}){Reset} {message}")
        
            if loglevel >= self.fileLogLevel:
                with open(self.logfile, "a", encoding=self.encoding) as f:
                    print(f"({self.pid}) {f"{datetime.now():%F %X.%f}"[:-3]} [{loglevel.name:5}]{self.func} {self.callerName}{callerFunc}({callerLine}) {message}", file=f)

        except Exception as ex:

            raise MapleLoggerException(f"Failed to write log: {ex}") from ex

        if self.maxLogSize > 0:

            # Check file size

            try:

                if path.exists(self.logfile) and path.getsize(self.logfile) > self.maxLogSize:

                    # Rename log file

                    if self.fileMode == "overwrite":

                        if path.isfile(f"{self.logfile}_old.log"):

                            os.remove(f"{self.logfile}_old.log")

                        os.rename(self.logfile, f"{self.logfile}_old.log")
                        return

                    elif self.fileMode == "daily":

                        dateStr = ""

                    else:

                        dateStr = f"_{datetime.now():%Y%m%d_%H%M%S}"
                    
                    i = 0
                    logCopyFile = f"{self.logfile}{dateStr}{i}.log"

                    while path.isfile(logCopyFile):

                        i += 1
                        logCopyFile = f"{self.logfile}{dateStr}{i}.log"

                    os.rename(self.logfile, logCopyFile)

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

        self.logWriter(logLevel, ex, callerDepth=2)
        self.logWriter(logLevel, traceback.format_exc(), callerDepth=2)

    #
    ################################
    # Save log settings

    def saveLogSettings(self, configFile: str = "config.json") -> None:

        """Save current log settings to config file"""
        
        try:

            # Set config file path

            if path.isabs(configFile):

                configFilePath = configFile

            else:

                configFilePath = path.join(os.getcwd(), configFile)

            # Try to read config file

            logConfInstance = MapleJson(configFilePath)

            if path.isfile(configFilePath):

                confJson = logConfInstance.read()

            else:

                confJson = {}

            # Update configuration

            logConf = confJson.get(self.CONFIG_KEY, None)

            if logConf is None:

                logConf = {}

            logConf[self.CONSOLE_LOG_LEVEL] = self.LogLevel(self.consoleLogLevel).name
            logConf[self.FILE_LOG_LEVEL] = self.LogLevel(self.fileLogLevel).name
            logConf[self.MAX_LOG_SIZE] = self.maxLogSize / 1000000
            logConf[self.WORKING_DIRECTORY] = self.CWD

            confJson[self.CONFIG_KEY] = logConf

            # Save config file

            logConfInstance.write(confJson)

        except Exception as e:

            raise MapleLoggerException(f"Error saving logger config file: {e}") from e

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

""" * * * * * * * * * * * * * """
"""
ToDo list:

* Logger *

- Add option to set date format
- Add set* functions
- Configure log format in config file

"""
""" * * * * * * * * * * * * * """
