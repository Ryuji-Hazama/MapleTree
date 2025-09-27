import datetime
from enum import IntEnum
from cryptography.fernet import Fernet
import inspect
from os import path, remove, getpid
import os
from shutil import move
import subprocess
import traceback
import uuid

################################
# Exception classes

class MapleException(Exception):

    """Basic exception for all exception inside the Maple tree."""

class MapleFileNotFoundException(MapleException):

    def __init__(self, mapleFile: str = "", message: str = "Maple file not found"):

        self.message = f"{message}: {mapleFile}"
        super().__init__(self.message)

class KeyEmptyException(MapleException):

    def __init__(self, mapleFile: str = "", message: str | None = None):

        if message is None:

            self.message = "File encryption toggle was set as \"True\", but the encryption key was not set.\n" \
                           "Please set key(bytes) value or encryption toggle to \"False\"."
            
        else:

            self.message = message

        super().__init__(mapleFile, self.message)

class MapleFileLockedException(MapleException):

    def __init__(self, mapleFile: str = "", message: str = "Maple file has been locked by other instance"):

        self.message = f"{message}: {mapleFile}"
        super().__init__(self.message)

class MapleDataNotFoundException(MapleException):

    def __init__(self, fileName: str = "", message: str = "Data not found"):

        self.message = f"{message}: {fileName}"
        super().__init__(self.message)

class MapleHeaderNotFoundException(MapleDataNotFoundException):

    def __init__(self, fileName = "", header: str = "", preHeader: str = "", message = ""):

        if header != "":

            self.message = f"Header [{header}] not found"

        else:

            self.message = "Header not found"

        if preHeader != "":

            self.message = f"{self.message} in [{preHeader}]"

        if message != "":

            self.message = message

        super().__init__(fileName, self.message)

class MapleTagNotFoundException(MapleDataNotFoundException):

    def __init__(self, fileName = "", tag: str = "", header: str = "", message = ""):

        if tag != "":

            self.message = f"Tag [{tag}] not found"

        else:

            self.message = "Tag not found"

        if header != "":

            self.message = f"{self.message} in [{header}]"

        if message != "":

            self.message = message

        super().__init__(self.message, fileName)

class NotAMapleFileException(MapleException):

    def __init__(self, filePath: str = "", message: str = "The file is not a Maple file"):

        self.message = f"{message}: {filePath}"
        super().__init__(self.message)

class InvalidMapleFileFormatException(NotAMapleFileException):

    def __init__(self, mapleFile = "", message = "Invalid Maple file format"):

        self.message = f"[{message}: {mapleFile}]"
        super().__init__(self.message)

class MapleFileEmptyException(InvalidMapleFileFormatException):

    def __init__(self, mapleFile="", message="File is empty"):
        super().__init__(mapleFile, message)

#############################
# Main class

class MapleTree:

    def __init__(self, fileName: str, tabInd: int = 4, encrypt: bool = False, key: bytes | None = None, createBaseFile: bool = False):

        """
        key must be base_64 bytes.
        """

        self.TAB_FORMAT = " " * tabInd
        self.ENCRYPT = encrypt
        self.KEY = key
        self.fileName = fileName

        if encrypt and key is None:

            raise KeyEmptyException(fileName)

        f = None

        if createBaseFile and not path.isfile(fileName):

            # Create a base Maple file

            try:

                mapleBaseString = "MAPLE\nEOF"

                if encrypt:

                    # Encrypt data

                    mapleBaseString = Fernet(key).encrypt(mapleBaseString.encode()).decode()

                f = open(fileName, "w")
                f.write(mapleBaseString)
                f.close()

            except Exception as e:

                raise MapleException(e) from e
            
            finally:

                if f is not None:
                    f.close()

        try:

            f = open(fileName, "r")

            if encrypt:

                # Decode encryption
                
                fileData = f.read()
                fileData = Fernet(key).decrypt(fileData.encode()).decode()
                self.fileStream = fileData.split("\n")

                # Add \r at the end of each line

                for i, fileLine in enumerate(self.fileStream):

                    self.fileStream[i] = f"{fileLine}\n"

            else:
                    
                self.fileStream = f.readlines()

            # If the file is only one line or empty

            if len(self.fileStream) < 2:

                raise MapleFileEmptyException(fileName)
            
            # Search data region

            self.mapleIndex = self.fileStream.index("MAPLE\n")
            self.eofIndex = self._findEof(self.mapleIndex)

            # Check data format

            self._mapleFormatter()
            
        except MapleFileEmptyException:

            raise

        except FileNotFoundError as fnfe:

            raise MapleFileNotFoundException(fileName) from fnfe
        
        except ValueError or InvalidMapleFileFormatException as ve:

            raise InvalidMapleFileFormatException(fileName) from ve

        except Exception as ex:

            raise MapleException(ex) from ex
        
        finally:

            if f is not None:
                f.close()
        
    #
    ##############################
    # Lock file instance

    #
    ##############################
    # Unlock file instance

    #
    ##############################
    # Read file

    #
    ##############################
    # Encrypt data

    def __encryptData(self) -> str:

        """
        Return encrypted base_64 string
        """

        fileData = "".join(self.fileStream).encode()
        fileData = Fernet(self.KEY).encrypt(fileData).decode()

        return fileData

    #
    ##############################
    # Save to file

    def _saveToFile(self):

        f = None

        # Create file data

        try:

            if self.ENCRYPT:

                fileData = self.__encryptData()

            else:

                fileData = "".join(self.fileStream)

            f = open(self.fileName, "w")
            f.writelines(fileData)
            f.close()

        except Exception as e:

            raise MapleException(e) from e
        
        finally:

            if f is not None:
                f.close()

    #
    ##############################
    # Remove white space

    def __removeWhiteSpace(self, strLine: str) -> str:

        strLen = len(strLine)
        ind = 0

        while ind < strLen:

            if strLine[ind] != " " and strLine[ind] != "\t":
                break

            ind += 1

        return strLine[ind:strLen]

    #
    ################################
    # Get tag

    def __getTag(self, mapleLine: str) -> str:

        """Get a tag from a data line."""

        if mapleLine == "":
            return ""

        # Remove white space in front and add return at the end

        mapleLine = f"{self.__removeWhiteSpace(mapleLine)}\n"
        strLen = len(mapleLine)

        # Start read tag

        try:

            for ind in range(0, strLen):
            
                if mapleLine[ind] == " " or mapleLine[ind] == "\n" or mapleLine[ind] == "\r":
                    break
        
        except Exception as ex:

            raise MapleException from ex

        return mapleLine[:ind]

    #
    ###########################
    # Get value

    def __getValue(self, mapleLine: str) -> str:

        """Get a value from a data line."""

        ind = 0

        # Remove white space in front

        mapleLine = self.__removeWhiteSpace(mapleLine)
        strLen = len(mapleLine)
        
        if strLen < 2 or mapleLine == "":
            return ""

        # Remove tag

        try:
            for ind in range(0, strLen):

                if mapleLine[ind] == " " or mapleLine[ind] == "\n" or mapleLine[ind] == "\r":
                    ind += 1
                    break

        except Exception as ex:

            raise MapleException from ex

        # Return value

        if ind >= strLen - 1:

            return ""
        
        else:

            return mapleLine[ind:strLen - 1]
        
    #
    ####################################
    # Header not found exception handler

    def __headerNotFoundExceptionHandler(self, headInd: int, *headers: str) -> None:

        if headInd < 1:

            raise MapleHeaderNotFoundException(self.fileName, headers[headInd])
        
        else:

            raise MapleHeaderNotFoundException(self.fileName, headers[headInd], headers[headInd - 1])

    #
    #################################
    # Find EOF

    def _findEof(self, startInd: int) -> int:

        """"Find EOF line index"""

        listLen = len(self.fileStream)

        while startInd < listLen:

            startInd += 1
            
            if self.__getTag(self.fileStream[startInd]) == "EOF":

                return startInd
            
        raise InvalidMapleFileFormatException(self.fileName)

    #
    #################################
    # ToE

    def __ToE(self, curInd: int) -> int:

        """Return E tag line index of current level
        Raise"""

        while curInd < self.eofIndex:

            curInd += 1
            mapleTag = self.__getTag(self.fileStream[curInd])

            if mapleTag == "E":

                return curInd
            
            elif mapleTag == "H":

                curInd = self.__ToE(curInd)

        raise InvalidMapleFileFormatException(self.fileName)

    #
    ######################
    # Format maple file

    def _mapleFormatter(self, willSave: bool = False):

        """Format Maple stream
        and save to file if willSave is True"""

        try:

            ind = 0

            # Format

            for i, mapleLine in enumerate(self.fileStream, self.mapleIndex):

                mapleLine = self.__removeWhiteSpace(mapleLine)
                tag = self.__getTag(mapleLine)

                if tag == "EOF":

                    if ind != 0:

                        raise InvalidMapleFileFormatException(self.fileName, "EOF tag in the middle of the data")
                    
                    break

                elif tag == "E":

                    ind -= 1

                if ind < 0:

                    raise InvalidMapleFileFormatException(self.fileName)

                self.fileStream[i] = f"{self.TAB_FORMAT * ind}{mapleLine}"

                if tag == "H":

                    ind += 1

        except InvalidMapleFileFormatException:

            raise

        except Exception as ex:

            raise MapleException(ex) from ex
        
        # Save to file
        
        if willSave:
            
            self._saveToFile()

    #
    #################################
    # Find header

    def _findHeader(self, headers: list):

        """Serch header index.\n
        If the headers exist, return True, last header line index.\n
        If the headers does not exist, return False, E line index, last found headers index."""

        headCount = len(headers)
        ind = 0
        headInd = self.mapleIndex
        eInd = self.eofIndex

        # Find header

        try:

            while ind < headCount:

                header = f"{self.TAB_FORMAT * ind}H {headers[ind]}\n"
                headInd = self.fileStream.index(header, headInd, eInd)
                eInd = self.__ToE(headInd)

                ind += 1

            return True, eInd, headInd

        except ValueError:

            return False, eInd, ind
        
        except InvalidMapleFileFormatException:

            raise

        except Exception as e:
        
            raise MapleException(e) from e
        
    #
    #################################
    # Find tag line

    def _findTagLine(self, tag: str, headInd: int, eInd: int) -> int:

        while headInd < eInd:

            headInd += 1
            tagLine = self.__getTag(self.fileStream[headInd])

            if tagLine == "H":

                headInd = self.__ToE(headInd)

            elif tagLine == tag:

                return headInd
            
        raise MapleTagNotFoundException(self.fileName, tag)

    #
    #################################
    # Read tag line

    def readMapleTag(self, tag: str, *headers: str) -> str:

        '''
        Read a Maple file tag line value in headers
        '''

        headInd = self.mapleIndex
        eInd = self.eofIndex

        # Serch headers

        isFound, eInd, headInd = self._findHeader(headers)

        if not isFound:

            self.__headerNotFoundExceptionHandler(headInd, headers)

        # Find tag

        try:

            ind = self._findTagLine(tag, headInd, eInd)
            return self.__getValue(self.fileStream[ind])

        except MapleTagNotFoundException:

            return None
        
        except Exception as e:

            raise MapleException(e) from e

    #
    ###################################################
    # Save tag line

    def saveTagLine(self, tag: str, valueStr: str, willSave: bool, *headers: str) -> None:

        """Save valueStr to tag in headers.\n
        If the headers does not exist, create new headers.\n
        Overwrte file if sillSave == True"""

        # Find headers

        isHead, eInd, headInd = self._findHeader(headers)

        if not isHead:

            # Create new headers

            headLen = len(headers)

            while headInd < headLen:

                self.fileStream.insert(eInd, f"H {headers[headInd]}\n")
                eInd += 1
                self.fileStream.insert(eInd, "E\n")
                headInd += 1

            tagInd = eInd

        else:

            # Find tag

            try:

                tagInd = self._findTagLine(tag, headInd, eInd)

            except MapleTagNotFoundException:

                # If the tag does not exist

                tagInd = eInd

            except Exception as e:

                raise MapleException(e) from e
            
        # Save tag line

        if tagInd == eInd:

            # If it is a new line

            self.fileStream.insert(tagInd, f"{tag} {valueStr}\n")

        else:

            # Overwite

            self.fileStream[tagInd] = f"{tag} {valueStr}\n"

        # Save?

        self._mapleFormatter(willSave)

        # Refresh EOF index

        self.eofIndex = self._findEof(self.eofIndex - 1)

    #
    #############################
    # Delete tag line

    def deleteTag(self, delTag: str, willSave: bool = False, *headers: str) -> bool:

        """
        Delete tag(delTag) from header(headers) in Maple file(delFile)\n
        Return True if it success.
        """

        try:

            gotHeader, eInd, headInd = self._findHeader(headers)

            if not gotHeader:

                self.__headerNotFoundExceptionHandler(headInd, headers)

            tagInd = self._findTagLine(delTag, headInd, eInd)
            self.fileStream.pop(tagInd)

            # Save?

            if willSave:

                self._saveToFile()

            # Refresh EOF index

            self.eofIndex = self._findEof(tagInd)

        except MapleDataNotFoundException as dnfe:

            raise MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise MapleException(ex) from ex
        
        return True
    #
    ############################
    # Get tag value dictioanry

    def getTagValueDic(self, *headers: str) -> dict[str:str]:

        """Get and return tag:value dictionary from headers in Maple file"""

        retDic = {}

        try:

            # Find header

            gotHeader, eInd, headInd = self._findHeader(headers)

            if not gotHeader:

                self.__headerNotFoundExceptionHandler(headInd, headers)

            # Get tag and values

            while headInd < eInd - 1:

                headInd += 1
                lineTag = self.__getTag(self.fileStream[headInd])

                if lineTag == "H":

                    headInd = self.__ToE(headInd)

                else:

                    retDic[lineTag] = self.__getValue(self.fileStream[headInd])

            return retDic
        
        except MapleDataNotFoundException as dnfe:

            raise MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise MapleException(ex) from ex

    #
    ############################
    # Get tags list

    def getTags(self, *headers: str) -> list[str]:

        """
        Get and return tags list from headers in Maple file(readFile)
        """

        retList = []

        try:

            # Find header
                
            gotHeader, eInd, headInd = self._findHeader(headers)

            if not gotHeader:

                self.__headerNotFoundExceptionHandler(headInd, headers)

            # Get tag list

            while headInd < eInd - 1:

                headInd += 1
                lineTag = self.__getTag(self.fileStream[headInd])

                if lineTag == "H":

                    headInd = self.__ToE(headInd)

                else:

                    retList.append(lineTag)

            return retList
        
        except MapleDataNotFoundException as dnfe:

            raise MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise MapleException(ex) from ex

    #
    #############################
    # Delete header

    def deleteHeader(self, delHead: str, willSave: bool = False, *Headers: str) -> bool:

        try:

            gotHeader, eInd, headInd = self._findHeader(Headers)

            if not gotHeader:

                self.__headerNotFoundExceptionHandler(headInd, Headers)

            headInd = self.fileStream.index(f"{self.TAB_FORMAT * len(Headers)}H {delHead}\n", headInd, eInd)
            eInd = self.__ToE(headInd)

            self.fileStream = self.fileStream[:headInd] + self.fileStream[eInd + 1:]

            # Save?

            if willSave:

                self._saveToFile()

            # Refresh EOF index

            self.eofIndex = self._findEof(headInd + 1)

        except ValueError or MapleDataNotFoundException as ve:

            raise MapleDataNotFoundException(self.fileName) from ve
        
        except Exception as e:

            raise MapleException(e) from e
        
        return True

    #
    ############################
    # Get headers list

    def getHeaders(self, *headers: str) -> list:

        """
        Get and return headers list from headers in Maple file(readFile)
        """

        retList = []

        try:

            gotHeader, eInd, headInd = self._findHeader(headers)

            if not gotHeader:

                self.__headerNotFoundExceptionHandler(headInd, headers)

            while headInd < eInd:

                headInd += 1
                fileLine = self.__removeWhiteSpace(self.fileStream[headInd])

                if fileLine.startswith("H "):

                    retList.append(self.__getValue(fileLine))
                    headInd = self.__ToE(headInd)

        except MapleDataNotFoundException as dnfe:

            raise MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise MapleException(ex) from ex
        
        return retList

class Logger:

    def __init__(self, func: str = "", workingDirectory: str | None = None, cmdLogLevel: str | None = None, fileLogLevel: str | None = None, maxLogSize: float | None = None):

        """
        Set a negative value to maxLogSize for an infinite log file size.
        """

        self.intMaxValue = 4294967295
        self.consoleLogLevel = -1
        self.fileLogLevel = -1
        self.func = func
        self.CWD = os.getcwd()
        
        configFile = path.join(self.CWD, "config.mpl")

        #
        ############################
        # Check config file

        try:

            if not path.isfile(configFile):

                f = open(configFile, "w")
                f.write("MAPLE\n"
                        "H *LOG_SETTINGS\n"
                        "    CMD INFO\n"
                        "    FLE INFO\n"
                        "    MAX 3\n"
                        "    OUT \n"
                        "    CMT TRACE, DEBUG, INFO, WARN, ERROR, FATAL\n"
                        "E\nEOF")
                f.close()
                
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
        
        self.logfile = path.join(self.CWD, f"log_{datetime.datetime.now():%Y%m%d}.log")

        #
        ############################
        # Check log directory

        if not path.isdir(path.join(self.CWD)):
            os.makedirs(path.join(self.CWD))

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

    def logWriter(self, loglevel: LogLevel, message: any):

        """
        Output log to log file and console.
        """

        ''' - - - - - - -*
        *                *
        * Logging Object *
        *                *
        * - - - - - - -'''

        f = open(self.logfile, "a")

        # Get caller informations

        callerFunc = inspect.stack()[1].function
        callerLine = inspect.stack()[1].lineno

        try:

            # Export to console and log file

            if loglevel >= self.consoleLogLevel:
                print(f"[{loglevel.name:5}][{self.func}] {callerFunc}({callerLine}) {message}")
        
            if loglevel >= self.fileLogLevel:
                print(f"({getpid()}) {datetime.datetime.now():%Y-%m-%d %H:%M:%S} [{loglevel.name:5}][{self.func}] {callerFunc}({callerLine}) {message}", file=f)

        except Exception as ex:

            # If faled to export, print error info to console

            print(f"[ERROR] {ex}")

        finally:
            f.close()

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
                print(f"[ERROR] {ex}")

    #
    ################################
    # Error messages

    def ShowError(self, ex: Exception, message: str | None = None):

        '''Show and log error'''

        if message is not None:

            self.logWriter(self.LogLevel.ERROR, message)

        self.logWriter(self.LogLevel.ERROR, ex)
        self.logWriter(self.LogLevel.ERROR, traceback.format_exc())

#
############################
# Hide files and directories

def winHide(*fdPath):

    """
    Hide file in Windows
    """

    try:

        for hPath in fdPath:

            subprocess.run(f"attrib +H {hPath}", shell=True)

    except Exception as ex:

        print(ex)
        raise

#
##############################
# Unhide files and directories

def winUnHide(*fdPath):

    """
    Unhide file in Windows
    """

    try:

        for hPath in fdPath:

            subprocess.run(f"attrib -H {hPath}", shell=True)

    except Exception as ex:

        print(ex)
        raise