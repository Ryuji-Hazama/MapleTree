from datetime import datetime
import inspect
import os
from os import path
import sys
import traceback
from enum import IntEnum
from typing import Literal
from .json import MapleJson
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

        try:

            # Check the OS (Windows 10 or older cannot change the console color)

            if hasattr(sys, "getwindowsversion") and sys.getwindowsversion().build < 22000:

                self.consoleColors = ConsoleColors(Black="", Red="", Green="", Yellow="", Blue="", Magenta="", LightBlue="", White="",
                                                bgBlack="", bgRed="", bgGreen="", bgYellow="", bgBlue="", bgMagenta="", bgLightBlue="", bgWhite="",
                                                bBlack="", bRed="", bGreen="", bYellow="", bBlue="", bMagenta="", bLightBlue="", bWhite="",
                                                Bold="", Underline="", Reversed="", Reset="")

            logConfInstance = self.__checkConfigFile(configFile)
            self.__checkOutputDirectory(workingDirectory)
            self.__setLogFileName(self.fileMode)
            self.__setFuncName(kwargs.get("getLogger", False), func)
            self.__setLogFileSize(maxLogSize)
            self.__setOutputLogLevels(cmdLogLevel, fileLogLevel)
            self.__setFileEncoding(encoding)
            self.__saveLogSettings(logConfInstance)

        except Exception as ex:

            print(f"{self.consoleColors.Red}Error initializing logger: {ex}{self.consoleColors.Reset}")
            raise MapleLoggerException(f"Error initializing logger: {ex}") from ex

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

    ###########################################
    # Special Methods for Class Initialization

    def __checkConfigFile(self, configFile: str) -> MapleJson | None:
    
        '''Check logger config file and read settings'''

        self.CONFIG_KEY = "MapleLogger"
        self.CONSOLE_LOG_LEVEL = "ConsoleLogLevel"
        self.FILE_LOG_LEVEL = "FileLogLevel"
        self.MAX_LOG_SIZE = "MaxLogSize"
        self.WORKING_DIRECTORY = "WorkingDirectory"
        self.FILE_ENCODING = "FileEncoding"

        # Set config file path
        
        self.configFile = self.__checkFilePath(configFile)

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

        self.logConf = logConf
        return logConfInstance

    def __checkFilePath(self, filePath: str) -> str:

        '''Check and return absolute file path'''

        if path.isabs(filePath):

            return filePath

        else:

            return path.join(os.getcwd(), filePath)

    def __checkOutputDirectory(self, outputDir: str) -> None:

        '''Check and set output directory'''

        # Check parameter and config file

        if outputDir is not None:

            self.CWD = outputDir

        else:

            self.CWD = self.logConf.get(self.WORKING_DIRECTORY, None)

        # Set absolute path

        if self.CWD in {"", None}:

            self.CWD = path.join(os.getcwd(), "logs")
            self.logConf[self.WORKING_DIRECTORY] = self.CWD

        elif not path.isabs(self.CWD):

            self.CWD = path.join(os.getcwd(), self.CWD)

        # Check if directory exists

        if not path.isdir(self.CWD):

            os.makedirs(self.CWD)

    def __setLogFileName(self, fileMode: str) -> None:

        '''Set log file name'''

        if fileMode == "daily":

            self.logfile = path.join(self.CWD, f"log_{datetime.now():%Y%m%d}.log")
        
        else:

            self.logfile = path.join(self.CWD, "AppLog.log")

    def __setFuncName(self, isGetLogger: bool, func: str | None = None) -> None:

        if isGetLogger:

            caller = inspect.stack()[3].frame.f_globals.get("__name__", "")

        else:

            caller = inspect.stack()[2].frame.f_globals.get("__name__", "")

        if func in {None, ""}:

            self.func = ""
            self.callerName = ""
        
        elif func != caller:

            self.func = f"[{func}]"
            self.callerName = ""

        else:

            self.func = ""
            self.callerName = f"{caller}."

    def __setLogFileSize(self, maxLogSize: any) -> None:

        self.maxLogSize = 0

        if maxLogSize is not None:

            self.setMaxLogSize(maxLogSize)

        else:

            try:

                logSize = self.logConf.get(self.MAX_LOG_SIZE, None)

                if logSize is not None:

                    self.setMaxLogSize(logSize)

                else:

                    self.maxLogSize = 3000000
                    self.logConf[self.MAX_LOG_SIZE] = 3

            except MapleLoggerException as ex:

                print(f"{self.consoleColors.Red}Warning: Invalid MaxLogSize value provided. Using default value.{self.consoleColors.Reset}")
                self.maxLogSize = 3000000

        if self.maxLogSize == 0:

            print(f"{self.consoleColors.Red}Warning: Infinite log file size is not recommended. Using default value.{self.consoleColors.Reset}")
            self.maxLogSize = 3000000

    def __setOutputLogLevels(self, cmdLogLevel: any, fileLogLevel: any) -> None:

        self.consoleLogLevel = self.__setLogLevel(self.CONSOLE_LOG_LEVEL, cmdLogLevel)
        self.fileLogLevel = self.__setLogLevel(self.FILE_LOG_LEVEL, fileLogLevel)

    def __setLogLevel(self, fileOrConsole, loglevel: any) -> LogLevel:

        '''Set log level'''

        if loglevel is not None:

            tempLogLevel = loglevel
        
        else:

            tempLogLevel = self.logConf.get(fileOrConsole, "INFO")

            if tempLogLevel is None:

                tempLogLevel = "INFO"
                self.logConf[fileOrConsole] = tempLogLevel

        try:

            return self.toLogLevel(tempLogLevel)

        except MapleInvalidLoggerLevelException as ex:

            print(f"{self.consoleColors.Red}Warning: Invalid {fileOrConsole} provided: [{tempLogLevel}]. Using default value.{self.consoleColors.Reset}")
            return self.LogLevel.INFO

    def __setFileEncoding(self, encoding: str) -> None:

        if encoding is not None:

            self.encoding = encoding

        else:

            fileEncoding = self.logConf.get(self.FILE_ENCODING, None)

            if fileEncoding is None:

                fileEncoding = "utf-8"
                self.logConf[self.FILE_ENCODING] = fileEncoding

            self.encoding = fileEncoding

    def __saveLogSettings(self, logConfInstance: MapleJson | None) -> None:

        """ Save current log settings to config file """

        if logConfInstance is not None:

            try:

                confJson = logConfInstance.read()

            except Exception:

                confJson = {}
            
            try:

                confJson[self.CONFIG_KEY] = self.logConf
                logConfInstance.write(confJson)

            except Exception as ex:

                print(f"{self.consoleColors.Red}Warning: Failed to write logger config file: {ex}{self.consoleColors.Reset}")

    # Class initialization ends here
    #################################

    #################################
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

        '''Check if string is a valid log level'''

        logLevelStr = lLStr.upper()

        for lLevel in self.LogLevel:
            if logLevelStr == lLevel.name:
                return lLevel

        return -1

    #
    #################################
    # Logger

    def logWriter(self, loglevel: LogLevel, message: any, callerDepth: int = 1) -> None:

        """
        Output log to log file and console.
        """

        # Precheck log level

        if loglevel < self.consoleLogLevel and loglevel < self.fileLogLevel:

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

            if loglevel >= self.consoleLogLevel:
                print(f"[{col}{loglevel.name:5}{Reset}]{Green}{self.func}{Reset} {bBlack}{callerFunc}({callerLine}){Reset} {message}")
        
            if loglevel >= self.fileLogLevel:

                for i in range(3):

                    try:

                        with open(self.logfile, "a", encoding=self.encoding) as f:
                            print(f"({self.pid}) {f"{datetime.now():%F %X.%f}"[:-3]} [{loglevel.name:5}]{self.func} {self.callerName}{callerFunc}({callerLine}) {message}", file=f)

                        break

                    except IOError:

                        if i == 2:
                            raise

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

    def saveLogSettings(self, configFile: str = None) -> None:

        """Save current log settings to config file"""
        
        try:

            # Set config file path

            if configFile is None:

                configFile = self.configFile

            configFilePath = self.__checkFilePath(configFile)

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
