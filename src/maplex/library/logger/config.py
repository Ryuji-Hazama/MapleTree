"""
Move configu helper functions to a separate file to avoid circular imports and improve code organization
"""

from datetime import datetime
import inspect
from typing import Literal
import os
from os import path
import pathlib
from pydantic import BaseModel
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from mapleColors import ConsoleColors
from mapleExceptions import *
from jsonHandler import MapleJson
from .consts import *
from .utilities import *
from library.logger.log_levels import LogLevel


class TimeStamp(BaseModel):

    timestampFormat: str | None = None
    digits: int | None = None

class Formats(BaseModel):

    consoleFormat: str | None = None
    fileFormat: str | None = None
    timestamp: TimeStamp | None = None

class LoggerConfig(BaseModel):

    func: str | None = None
    callerName: str | None = None
    workingDirectory: str | None = None
    consoleLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None
    fileLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None
    maxLogSize: int | None = None
    fileMode: Literal["append", "overwrite", "daily"] | None = None
    configFile: str = "config.json"
    encoding: str | None = None
    getLogger: bool | None = None
    consoleAlignWidth: int | None = None
    fileAlignWidth: int | None = None
    formats: Formats | None = None

    logConfInstance: None = None
    logConf: dict[str, object] | None = None
    logfile: str | None = None
    pid: int = os.getpid()

    consoleColors: ConsoleColors | None = None

    def __init__(self, config: dict[str, object]) -> None:

        try:

            super().__init__(**config)
            self.consoleColors = getConsoleColors()
            self.logConfInstance = self.checkConfigFile(config.get(CONFIG_FILE, self.configFile))
            self.checkOutputDirectory(config.get(WORKING_DIRECTORY, None))
            self.setLogFileName(config.get(FILE_MODE, "append"))
            self.setFuncName(config.get(GET_LOGGER, False), config.get(FUNC, None))
            self.setAlignWidth(config.get(CONSOLE_ALIGN_WIDTH, None), config.get(FILE_ALIGN_WIDTH, None))
            self.setLogFileSize(config.get(MAX_LOG_SIZE, None))
            self.setOutputLogLevels(config.get(CONSOLE_LOG_LEVEL, None), config.get(FILE_LOG_LEVEL, None))
            self.setFileEncoding(config.get(FILE_ENCODING, None))
            self.setTimestampFormat(config.get(PARAM_TIMESTAMP, None))
            self.setOutputFormat(config.get(CONSOLE_LOG_FORMAT, None), config.get(FILE_LOG_FORMAT, None))
            self.saveLogSettings(self.logConfInstance)

        except Exception as ex:

            print(ex)
            print(f"{self.consoleColors.Red}Error: Failed to initialize logger config: {ex}{self.consoleColors.Reset}")
            raise ex

    
    def checkConfigFile(self, configFile: str) -> MapleJson | None:
    
        # Set config file path
        
        self.configFile = self.checkFilePath(configFile)

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

        logConf = confJson.get(CONFIG_KEY, None)

        if logConf is None:

            logConf = {}
            logConf[CONSOLE_LOG_LEVEL] = "INFO"
            logConf[FILE_LOG_LEVEL] = "INFO"
            logConf[MAX_LOG_SIZE] = 3
            logConf[WORKING_DIRECTORY] = "logs"

        self.logConf = logConf
        return logConfInstance

    def checkFilePath(self, filePath: str) -> str:

        '''Check and return absolute file path'''

        if path.isabs(filePath):

            return filePath

        else:

            return path.join(os.getcwd(), filePath)

    def checkOutputDirectory(self, outputDir: str) -> None:

        '''Check and set output directory'''

        # Check parameter and config file

        if outputDir is not None:

            self.workingDirectory = outputDir

        else:

            self.workingDirectory = self.logConf.get(WORKING_DIRECTORY, None)

        # Set absolute path

        if self.workingDirectory in {"", None}:

            self.workingDirectory = path.join(os.getcwd(), "logs")
            self.logConf[WORKING_DIRECTORY] = self.workingDirectory

        elif not path.isabs(self.workingDirectory):

            self.workingDirectory = path.join(os.getcwd(), self.workingDirectory)

        # Check if directory exists

        if not path.isdir(self.workingDirectory):

            os.makedirs(self.workingDirectory)

    def setLogFileName(self, fileMode: str) -> None:

        '''Set log file name'''

        if fileMode == "daily":

            self.logfile = path.join(self.workingDirectory, f"log_{datetime.now():%Y%m%d}.log")
        
        else:

            self.logfile = path.join(self.workingDirectory, "AppLog.log")

    def setFuncName(self, isGetLogger: bool, func: str | None = None) -> None:

        if isGetLogger:

            caller = inspect.stack()[4].frame.f_globals.get("__name__", "")

        else:

            caller = inspect.stack()[3].frame.f_globals.get("__name__", "")

        if func in {None, ""}:

            self.func = ""
            self.callerName = ""
        
        elif func != caller:

            self.func = f"[{func}]"
            self.callerName = ""

        else:

            self.func = ""
            self.callerName = f"{caller}."

    def setAlignWidth(self, consoleAlignWidth: int | None = None, fileAlignWidth: int | None = None) -> None:

        '''Set function name alignment width'''

        if consoleAlignWidth is not None and type(consoleAlignWidth) is int and consoleAlignWidth > 0:

            self.consoleAlignWidth = consoleAlignWidth

        else:

            self.consoleAlignWidth = 16

        if fileAlignWidth is not None and type(fileAlignWidth) is int and fileAlignWidth > 0:

            self.fileAlignWidth = fileAlignWidth

        else:

            self.fileAlignWidth = 4

    def setLogFileSize(self, maxLogSize: object) -> None:

        self.maxLogSize = 0

        if maxLogSize is not None:

            self.setMaxLogSize(maxLogSize)

        else:

            try:

                logSize = self.logConf.get(MAX_LOG_SIZE, None)

                if logSize is not None:

                    self.setMaxLogSize(logSize)

                else:

                    self.maxLogSize = 3000000
                    self.logConf[MAX_LOG_SIZE] = 3

            except MapleLoggerException as ex:

                print(f"{self.consoleColors.Red}Warning: Invalid MaxLogSize value provided. Using default value.{self.consoleColors.Reset}")
                self.maxLogSize = 3000000

        if self.maxLogSize == 0:

            print(f"{self.consoleColors.Red}Warning: Infinite log file size is not recommended. Using default value.{self.consoleColors.Reset}")
            self.maxLogSize = 3000000

    def getLogLevel(self) -> None:

        '''
        Get LogLevel configuration from config file.
        Set namespace specific LogLevel if available, otherwise set default LogLevel.
        '''

        namespaceSettings = self.logConf.get(NAME_SPACES, [])
        thisNamespaceSettings = next((ns for ns in namespaceSettings if ns.get(NAME_SPACE) == self.callerName), None)

        if thisNamespaceSettings is not None:

            self.consoleLogLevel = thisNamespaceSettings.get(CONSOLE_LOG_LEVEL, None)
            self.fileLogLevel = thisNamespaceSettings.get(FILE_LOG_LEVEL, None)

    def setOutputLogLevels(self, cmdLogLevel: object, fileLogLevel: object) -> None:

        self.getLogLevel()
        self.consoleLogLevel = self.__setLogLevel(CONSOLE_LOG_LEVEL, cmdLogLevel if self.consoleLogLevel is None else self.consoleLogLevel)
        self.fileLogLevel = self.__setLogLevel(FILE_LOG_LEVEL, fileLogLevel if self.fileLogLevel is None else self.fileLogLevel)

    def __setLogLevel(self, fileOrConsole, loglevel: object) -> LogLevel:

        '''Set log level'''

        if loglevel is not None:

            tempLogLevel = loglevel
        
        else:

            tempLogLevel = self.logConf.get(fileOrConsole, None)

            if tempLogLevel is None:

                tempLogLevel = "INFO"
                self.logConf[fileOrConsole] = tempLogLevel

        try:

            return toLogLevel(tempLogLevel)

        except MapleInvalidLoggerLevelException as ex:

            print(f"{self.consoleColors.Red}Warning: Invalid {fileOrConsole} provided: [{tempLogLevel}]. Using default value.{self.consoleColors.Reset}")
            return self.LogLevel.INFO

    def setFileEncoding(self, encoding: str) -> None:

        if encoding is not None:

            self.encoding = encoding

        else:

            fileEncoding = self.logConf.get(FILE_ENCODING, None)

            if fileEncoding is None:

                fileEncoding = "utf-8"
                self.logConf[FILE_ENCODING] = fileEncoding

            self.encoding = fileEncoding

    def setTimestampFormat(self, timestampFormat: dict) -> None:

        """Set timestamp format for logs. Default is "%F %X.%f" (e.g. 2024-06-01 12:34:56.789). You can set this in config file with key "TimestampFormat"."""

        if self.formats is None:

            self.formats = Formats()

        if self.formats.timestamp is None:

            self.formats.timestamp = TimeStamp()

        if timestampFormat is not None:

            self.formats.timestamp.timestampFormat = timestampFormat.get(FORMAT, None)
            self.formats.timestamp.digits = timestampFormat.get(DIGITS, 3)

        else:

            timestampSettings = self.logConf.get(FORMATS, {}).get(TIMESTAMP, {})
            configTimestampFormat = timestampSettings.get(FORMAT, None)
            configTimestampDigits = timestampSettings.get(DIGITS, None)

            if configTimestampFormat is None:

                configTimestampFormat = TIMESTAMP_FORMAT
                timestampSettings[FORMAT] = configTimestampFormat
                self.logConf.setdefault(FORMATS, {})[TIMESTAMP] = timestampSettings

            if configTimestampDigits is None:

                configTimestampDigits = MILLISECOND_DIGITS
                timestampSettings[DIGITS] = configTimestampDigits
                self.logConf.setdefault(FORMATS, {})[TIMESTAMP] = timestampSettings

            if "TimestampFormat" in self.logConf:

                # Show warning if old config key is used
                print(f"{self.consoleColors.Yellow}Warning: 'TimestampFormat' key in config file is deprecated. Please use 'Formats.Timestamp' instead.{self.consoleColors.Reset}\nMore details: https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_Logger.md#settings")

            self.formats.timestamp.timestampFormat = configTimestampFormat
            self.formats.timestamp.digits = configTimestampDigits

    def setOutputFormat(self, consoleFormat: str, fileFormat: str) -> None:

        """Set output format for console and file logs. Default is "[{level}]{func} {callerFunc}{callerLine}" for console and "({pid}) {timestamp} [{level}]{func} {callerName}{callerFunc}({callerLine})" for file. You can set this in config file with keys "ConsoleLogFormat" and "FileLogFormat"."""

        if self.formats is None:

            self.formats = Formats()

        if consoleFormat is not None:

            self.formats.consoleFormat = consoleFormat

        else:

            self.formats.consoleFormat = self.logConf.get(CONSOLE_LOG_FORMAT, None)

            if self.formats.consoleFormat is None:

                self.formats.consoleFormat = CONSOLE_FORMAT
                formatConf = self.logConf.get(FORMATS, {})
                formatConf[CONSOLE_LOG_FORMAT] = CONSOLE_FORMAT
                self.logConf[FORMATS] = formatConf

        if fileFormat is not None:

            self.formats.fileFormat = fileFormat

        else:

            self.formats.fileFormat = self.logConf.get(FILE_LOG_FORMAT, None)

            if self.formats.fileFormat is None:

                self.formats.fileFormat = FILE_FORMAT
                formatConf = self.logConf.get(FORMATS, {})
                formatConf[FILE_LOG_FORMAT] = FILE_FORMAT
                self.logConf[FORMATS] = formatConf

    def saveLogSettings(self, logConfInstance: MapleJson | None) -> None:

        """ Save current log settings to config file """

        if logConfInstance is not None:

            try:

                confJson = logConfInstance.read()

            except Exception:

                confJson = {}
            
            try:

                confJson[CONFIG_KEY] = self.logConf
                logConfInstance.write(confJson)

            except Exception as ex:

                print(f"{self.consoleColors.Red}Warning: Failed to write logger config file: {ex}{self.consoleColors.Reset}")

    def serialize(self) -> dict[str, object]:

        '''Serialize logger config to a dictionary'''

        return {
            FUNC: self.func,
            CALLER_NAME: self.callerName,
            WORKING_DIRECTORY: self.workingDirectory,
            CONSOLE_LOG_LEVEL: self.consoleLogLevel.name if self.consoleLogLevel else None,
            FILE_LOG_LEVEL: self.fileLogLevel.name if self.fileLogLevel else None,
            MAX_LOG_SIZE: self.maxLogSize,
            FILE_MODE: "daily" if self.logfile and "log_" in self.logfile else "append",
            FILE_ENCODING: self.encoding,
            TIMESTAMP: self.formats.timestamp if self.formats.timestamp else None,
            GET_LOGGER: bool(self.func),
            CONSOLE_ALIGN_WIDTH: self.consoleAlignWidth,
            FILE_ALIGN_WIDTH: self.fileAlignWidth,
            PARAM_CONSOLE_FORMAT: self.formats.consoleFormat,
            PARAM_FILE_FORMAT: self.formats.fileFormat,
            PROCESS_ID: self.pid
        }

    ###########################
    # Seters and getters

    def setMaxLogSize(self, maxLogSize: object) -> None:

        '''Set max log size'''

        try:

            self.maxLogSize = toLogSize(maxLogSize)

        except MapleLoggerException as ex:

            raise MapleLoggerException("Invalid max log size. Log size must be an integer, float or string.") from ex
