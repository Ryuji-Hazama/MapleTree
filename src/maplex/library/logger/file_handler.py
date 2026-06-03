from datetime import datetime
import os
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from .consts import *
from mapleExceptions import MapleLoggerException

"""
File handler for logging.
"""

class FileHandler:
    
    """
    FileHandler handles log file size management for the Logger class. It checks the size of the log file and creates a new one if the size exceeds the specified limit.
    """

    def __init__(
            self,
            logFilePath: str,
            maxFileSize: int,
            fileMode: str
    ) -> None:

        """
        Initialize a FileHandler instance.

        :param logFilePath: The path to the log file.
        :param maxFileSize: The maximum size of the log file in bytes.
        """

        self.logFilePath = logFilePath
        self.maxFileSize = maxFileSize
        self.fileMode = fileMode

    def __file_size_exceeded(self) -> bool:

        """
        Check if the log file exists and if its size exceeds the maximum file size.
        :return: True if the file size exceeds the maximum, False otherwise.
        """
        
        if os.path.exists(self.logFilePath):
            
            fileSize = os.path.getsize(self.logFilePath)
            return fileSize >= self.maxFileSize

        return False

    def __overwrite_log_file(self) -> None:

        """
        Overwrite the log file by swapping the current log file with a new one.
        The old log file is renamed with "_old" suffix and a new log file is created with the original name.
        """

        oldLogFilePath = self.logFilePath + "_old"

        if os.path.exists(oldLogFilePath):
            os.remove(oldLogFilePath)

        os.rename(self.logFilePath, oldLogFilePath)

    async def check_file_size(self) -> None:

        """
        Check the log file size and create a new log file if the size exceeds the maximum file size.
        """

        try:

            if self.maxFileSize < 1 or not self.__file_size_exceeded():
                return
            
            if self.fileMode == FILE_MODE_OVERWRITE:

                self.__overwrite_log_file()
                return

            if self.fileMode == FILE_MODE_DAILY:

                dateStr = ""

            else:

                dateStr = f"_{datetime.now():%Y%m%d_%H%M%S}"

            i = 0
            logCopyFilePath = f"{self.logFilePath}{dateStr}{i}.log"

            while os.path.exists(logCopyFilePath):

                i += 1
                logCopyFilePath = f"{self.logFilePath}{dateStr}{i}.log"

            os.rename(self.logFilePath, logCopyFilePath)

        except Exception as e:

            raise MapleLoggerException(f"Failed to manage log file size: {e}")