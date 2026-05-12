"""
Move configu helper functions to a separate file to avoid circular imports and improve code organization
"""

from typing import Literal
from pydantic import BaseModel

from .consts import *
from ..json import MapleJson


class LoggerConfig(BaseModel):

    func: str | None = None
    workingDirectory: str | None = None
    cmdLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None
    fileLogLevel: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NONE"] | None = None
    maxLogSize: float | None = None
    fileMode: Literal["append", "overwrite", "daily"] | None = None
    configFile: str = "config.json"
    encoding: str | None = None
    timestampFormat: str | None = None
    getLogger: bool | None = None

    def __init__(self, config: dict[str, any]) -> None:

        self.config = config

    
    def __checkConfigFile(self, configFile: str) -> MapleJson | None:
    
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
