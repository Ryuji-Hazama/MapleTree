"""
Logger formatter module for MapleLogger.
Format log messages based on the specified format string and log level.
"""

from datetime import datetime
import inspect
import os

from .consts import *
from .log_levels import *
from .utilities import *

class Formatter:

    def __init__(
            self,
            config: dict
    ) -> None:

        """
        Initialize a Formatter instance.

        :param consoleFormat: Format string for console log messages.
        :param fileFormat: Format string for file log messages.
        :param timestampFormat: Format string for timestamps in log messages.
        """

        self.consoleColors = getConsoleColors()
        self.logLevel = LogLevel
        self.config = config
        self.consoleFormat = config.get(CONSOLE_FORMAT, CONSOLE_FORMAT)
        self.fileFormat = config.get(FILE_FORMAT, FILE_FORMAT)
        self.pid = os.getpid()
        self.COLOR_CODE_LENGTH = 5
        self.COLOR_CODE_RESET_LENGTH = 4
        self.consoleColorLength = self.__getColorCodeLength()

    def __getColorCodeLength(self) -> int:

        """
        Calculate the total length of color codes in the console format string.

        :return: The total length of color codes in the console format string.
        """

        colorCodeLength = 0
        colorCodeSetLength = self.COLOR_CODE_LENGTH + self.COLOR_CODE_RESET_LENGTH

        if '{timestamp}' in self.consoleFormat:

            colorCodeLength += colorCodeSetLength

        if '{func}' in self.consoleFormat:

            colorCodeLength += colorCodeSetLength

        if '{callerName}' in self.consoleFormat:

            colorCodeLength += colorCodeSetLength

        if '{callerFunc}' in self.consoleFormat:

            colorCodeLength += colorCodeSetLength

        if '{callerLine}' in self.consoleFormat:

            colorCodeLength += colorCodeSetLength

        return colorCodeLength

    def __getCurrentTimestamp(self, timestampFormat: str) -> str:

        """
        Get the current timestamp formatted according to the specified format string.

        :param timestampFormat: The format string for the timestamp.
        :return: The current timestamp as a formatted string.
        """

        return datetime.now().strftime(timestampFormat)

    def __getLogLevelColor(self, logLevel: LogLevel) -> str:

        """
        Get the color code for a given log level.

        :param logLevel: The log level for which to get the color code.
        :return: The color code corresponding to the log level.
        """

        match logLevel:

            case self.logLevel.TRACE:

                col = self.consoleColors.bBlack

            case self.logLevel.DEBUG:

                col = self.consoleColors.Green

            case self.logLevel.INFO:

                col = self.consoleColors.bLightBlue

            case self.logLevel.WARN:

                col = self.consoleColors.bRed

            case self.logLevel.ERROR:

                col = self.consoleColors.Red

            case self.logLevel.FATAL:

                col = self.consoleColors.Bold + self.consoleColors.Red

            case self.logLevel.NONE:

                col = self.consoleColors.Bold + self.consoleColors.Italic + self.consoleColors.Black

        return col


    def format_console(self, logLevel: LogLevel, callerDepth: int) -> str:

        """
        Format a log message for console output.

        :param logLevel: The log level of the message.
        :param callerDepth: The depth of the caller in the call stack.
        :return: The formatted log message for console output.
        """

        consoleFormat = self.consoleFormat
        callerFrame = inspect.stack()[callerDepth]
        additionalLength = 0

        if '{pid}' in consoleFormat:

            consoleFormat = consoleFormat.replace('{pid}', f'{self.pid}')

        if '{timestamp}' in consoleFormat:

            timestamp = self.__getCurrentTimestamp(self.config.get(TIMESTAMP_FORMAT, '%Y-%m-%d %H:%M:%S'))
            consoleFormat = consoleFormat.replace('{timestamp}', timestamp)

        if '{level}' in consoleFormat:

            levelColor = self.__getLogLevelColor(logLevel)
            consoleFormat = consoleFormat.replace('{level}', f'{levelColor}{logLevel.name:5}{self.consoleColors.Reset}')
            additionalLength += len(levelColor) + len(self.consoleColors.Reset)

        if '{func}' in consoleFormat:

            consoleFormat = consoleFormat.replace('{func}', f'{self.consoleColors.Green}{self.config.get(FUNC, "")}{self.consoleColors.Reset}')

        if '{callerName}' in consoleFormat:

            consoleFormat = consoleFormat.replace('{callerName}', f'{self.consoleColors.bBlack}{self.config.get(CALLER_NAME, "")}{self.consoleColors.Reset}')

        if '{callerFunc}' in consoleFormat:

            callerFunc = callerFrame.function
            consoleFormat = consoleFormat.replace('{callerFunc}', f'{self.consoleColors.bBlack}{callerFunc}{self.consoleColors.Reset}')

        if '{callerLine}' in consoleFormat:

            callerLine = callerFrame.lineno
            consoleFormat = consoleFormat.replace('{callerLine}', f'{self.consoleColors.bBlack}({callerLine}){self.consoleColors.Reset}')

        consoleLength = len(consoleFormat) - (self.consoleColorLength + additionalLength)
        alignStep = self.config.get(CONSOLE_ALIGN_WIDTH, 1)
        alignWidth = alignStep * (consoleLength // alignStep + (1 if consoleLength % alignStep != 0 else 0)) + (self.consoleColorLength + additionalLength)
        return f'{consoleFormat:<{alignWidth}}'

    def format_file(self, logLevel: LogLevel, callerDepth: int) -> str:

        """
        Format a log message for file output.

        :param logLevel: The log level of the message.
        :param callerDepth: The depth of the caller in the call stack.
        :return: The formatted log message for file output.
        """

        fileFormat = self.fileFormat
        callerFrame = inspect.stack()[callerDepth]

        if '{pid}' in fileFormat:

            fileFormat = fileFormat.replace('{pid}', f'{self.pid}')

        if '{timestamp}' in fileFormat:

            timestamp = self.__getCurrentTimestamp(self.config.get(TIMESTAMP_FORMAT, '%Y-%m-%d %H:%M:%S'))
            fileFormat = fileFormat.replace('{timestamp}', timestamp)

        if '{level}' in fileFormat:

            fileFormat = fileFormat.replace('{level}', f'{logLevel.name:5}')

        if '{func}' in fileFormat:

            fileFormat = fileFormat.replace('{func}', f'{self.config.get(FUNC, "")}')

        if '{callerName}' in fileFormat:

            fileFormat = fileFormat.replace('{callerName}', f'{self.config.get(CALLER_NAME, "")}')

        if '{callerFunc}' in fileFormat:

            callerFunc = callerFrame.function
            fileFormat = fileFormat.replace('{callerFunc}', f'{callerFunc}')

        if '{callerLine}' in fileFormat:

            callerLine = callerFrame.lineno
            fileFormat = fileFormat.replace('{callerLine}', f'({callerLine})')

        alignStep = self.config.get(FILE_ALIGN_WIDTH, 1)
        alignWidth = alignStep * (len(fileFormat) // alignStep + (1 if len(fileFormat) % alignStep != 0 else 0))
        return f'{fileFormat:<{alignWidth}}'