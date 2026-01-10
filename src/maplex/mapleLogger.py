from datetime import datetime
import inspect
import os
from os import path
import sys
import traceback
from enum import IntEnum
from typing import Literal
from .mapleTreeEditor import MapleTree
from .mapleColors import ConsoleColors

class Logger:

    def __init__(
            self,
            func: str = "",
            workingDirectory: str | None = None,
            cmdLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None,
            fileLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None,
            maxLogSize: float | None = None
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
        
        # Check the OS (Windows 10 or older cannot change the console color)

        if hasattr(sys, "getwindowsversion") and sys.getwindowsversion().build < 22000:

            self.consoleColors = ConsoleColors(Black="", Red="", Green="", Yellow="", Blue="", Magenta="", LightBlue="", White="",
                                            bgBlack="", bgRed="", bgGreen="", bgYellow="", bgBlue="", bgMagenta="", bgLightBlue="", bgWhite="",
                                            bBlack="", bRed="", bGreen="", bYellow="", bBlue="", bMagenta="", bLightBlue="", bWhite="",
                                            Bold="", Underline="", Reversed="", Reset="")

        #
        ############################
        # Check config file
        
        configFile = path.join(self.CWD, "config.mpl")

        try:

            if not path.isfile(configFile):

                with open(configFile, "w") as f:

                    f.write("MAPLE\n"
                            "H *LOG_SETTINGS\n"
                            "    CMD INFO\n"
                            "    FLE INFO\n"
                            "    # TRACE, DEBUG, INFO, WARN,\n"
                            "    # ERROR, FATAL, NONE\n"
                            "    MAX 3\n"
                            "    OUT logs\n"
                            "E\nEOF")
                
            maple = MapleTree(configFile)

        except:

            maple = None

        #
        ############################
        # Check output directory
        
        if workingDirectory is not None:

            self.CWD = workingDirectory

        elif maple:

            self.CWD = maple.readMapleTag("OUT", "*LOG_SETTINGS")

        if self.CWD in {"", None}:

            self.CWD = path.join(os.getcwd(), "logs")

        elif not path.isabs(self.CWD):

            self.CWD = path.join(os.getcwd(), self.CWD)

        self.logfile = path.join(self.CWD, f"log_{datetime.now():%Y%m%d}.log")

        #
        ############################
        # Check log directory

        if not path.isdir(path.join(self.CWD)):
            os.makedirs(path.join(self.CWD))

        #
        ############################
        # Set function name

        if func != "":

            self.func = f"[{func}]"

        else:

            self.func = ""

        #
        ############################
        # Set max log file size

        self.maxLogSize = 0

        if maxLogSize is not None:

            self.maxLogSize = maxLogSize * 1000000

        elif maple is not None:

            try:

                logSizeStr = maple.readMapleTag("MAX", "*LOG_SETTINGS")

                if logSizeStr != "":

                    self.maxLogSize = float(logSizeStr) * 1000000

            except:

                pass

        if self.maxLogSize == 0:

            self.maxLogSize = 3000000

        #
        ############################
        # Set output log levels

        self.consoleLogLevel = -1
        self.fileLogLevel = -1

        # Console log level

        if cmdLogLevel is not None:

            self.consoleLogLevel = self.isLogLevel(cmdLogLevel)

        if self.consoleLogLevel == -1 and maple is not None:

            strLogLevel = maple.readMapleTag("CMD", "*LOG_SETTINGS")

            if strLogLevel is not None:

                self.consoleLogLevel = self.isLogLevel(strLogLevel)

        if self.consoleLogLevel == -1:

            self.consoleLogLevel = self.LogLevel.INFO

        # File log level

        if fileLogLevel is not None:

            self.fileLogLevel = self.isLogLevel(fileLogLevel)

        if self.fileLogLevel == -1 and maple is not None:

            strLogLevel = maple.readMapleTag("FLE", "*LOG_SETTINGS")

            if strLogLevel is not None:

                self.fileLogLevel = self.isLogLevel(strLogLevel)

        if self.fileLogLevel == -1:

            self.fileLogLevel = self.LogLevel.INFO

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

                    col = Bold + Black

                case _:

                    col = ""

            # Export to console and log file

            if loglevel >= self.consoleLogLevel:
                print(f"[{col}{loglevel.name:5}{Reset}]{Green}{self.func}{Reset} {bBlack}{callerFunc}({callerLine}){Reset} {message}")
        
            if loglevel >= self.fileLogLevel:
                with open(self.logfile, "a") as f:
                    print(f"({self.pid}) {f"{datetime.now():%F %X.%f}"[:-3]} [{loglevel.name:5}]{self.func} {callerFunc}({callerLine}) {message}", file=f)

        except Exception as ex:

            # If faled to export, print error info to console

            print(f"{Red}[ERROR] {ex}{Reset}")

        if self.maxLogSize > 0:

            # Check file size

            try:

                if path.getsize(self.logfile) > self.maxLogSize:

                    i = 0
                    logCopyFile = f"{self.logfile}{i}.log"

                    while path.isfile(logCopyFile):

                        i += 1
                        logCopyFile = f"{self.logfile}{i}.log"

                    os.rename(self.logfile, logCopyFile)

            except Exception as ex:

                print(f"{Red}[ERROR] {ex}{Reset}")

    #
    ################################
    # Trace

    def Trace(self, object: any):

        '''Trace log'''

        self.logWriter(self.LogLevel.TRACE, object, callerDepth=2)
    #
    ################################
    # Debug

    def Debug(self, object: any):

        '''Debug log'''

        self.logWriter(self.LogLevel.DEBUG, object, callerDepth=2)

    #
    ################################
    # Info

    def Info(self, object: any):

        '''Info log'''

        self.logWriter(self.LogLevel.INFO, object, callerDepth=2)

    #
    ################################
    # Warn

    def Warn(self, object: any):

        '''Warn log'''

        self.logWriter(self.LogLevel.WARN, object, callerDepth=2)

    #
    ################################
    # Error

    def Error(self, object: any):

        '''Error log'''

        self.logWriter(self.LogLevel.ERROR, object, callerDepth=2)

    #
    ################################
    # Fatal

    def Fatal(self, object: any):

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

""" * * * * * * * * * * * * * """
"""
ToDo list:

* Logger *

- Configure log format in config file

"""
""" * * * * * * * * * * * * * """
