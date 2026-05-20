"""
Logger formatter module for MapleLogger.
Format log messages based on the specified format string and log level.
"""

from .utilities import *

class Formatter:

    def __init__(
            self,
            consoleFormat: str = '[{level}]{func} {callerFunc}({callerLine})',
            fileFormat: str = '({pid}) {timestamp} [{level}]{func} {callerName}.{callerFunc}({callerLine})'
    ) -> None:

        """
        Initialize a Formatter instance.

        :param consoleFormat: Format string for console log messages.
        :param fileFormat: Format string for file log messages.
        """

        self.consoleColors = getConsoleColors()
        self.consoleFormat = consoleFormat
        self.consoleColorLengh = self.__getColorLength(consoleFormat)
        self.fileFormat = fileFormat

    def __getColorLength(self, formatStr: str) -> int:

        """
        Calculate the length of color codes in the format string.

        :param formatStr: The format string to analyze.
        :return: The total length of color codes in the format string.
        """

        colorCodeLength = 0
        return colorCodeLength