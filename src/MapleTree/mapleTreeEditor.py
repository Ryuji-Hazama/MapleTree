import os.path as path
from cryptography.fernet import Fernet
from . import mapleExceptions as mExc

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

            raise mExc.KeyEmptyException(fileName)

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

                raise mExc.MapleException(e) from e
            
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

                raise mExc.MapleFileEmptyException(fileName)
            
            # Search data region

            self.mapleIndex = self.fileStream.index("MAPLE\n")
            self.eofIndex = self._findEof(self.mapleIndex)

            # Check data format

            self._mapleFormatter()
            
        except mExc.MapleFileEmptyException:

            raise

        except FileNotFoundError as fnfe:

            raise mExc.MapleFileNotFoundException(fileName) from fnfe
        
        except ValueError or mExc.InvalidMapleFileFormatException as ve:

            raise mExc.InvalidMapleFileFormatException(fileName) from ve
        except Exception as ex:

            raise mExc.MapleException(ex) from ex
        
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

            raise mExc.MapleException(e) from e
        
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

            raise mExc.MapleException from ex

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

            raise mExc.MapleException from ex

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

            raise mExc.MapleHeaderNotFoundException(self.fileName, headers[headInd])
        
        else:

            raise mExc.MapleHeaderNotFoundException(self.fileName, headers[headInd], headers[headInd - 1])
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
            
        raise mExc.InvalidMapleFileFormatException(self.fileName)

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

        raise mExc.InvalidMapleFileFormatException(self.fileName)

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

                        raise mExc.InvalidMapleFileFormatException(self.fileName, "EOF tag in the middle of the data")
                    
                    break

                elif tag == "E":

                    ind -= 1

                if ind < 0:

                    raise mExc.InvalidMapleFileFormatException(self.fileName)

                self.fileStream[i] = f"{self.TAB_FORMAT * ind}{mapleLine}"

                if tag == "H":

                    ind += 1

        except mExc.InvalidMapleFileFormatException:

            raise

        except Exception as ex:

            raise mExc.MapleException(ex) from ex
        
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
        
        except mExc.InvalidMapleFileFormatException:

            raise

        except Exception as e:
        
            raise mExc.MapleException(e) from e
        
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
            
        raise mExc.MapleTagNotFoundException(self.fileName, tag)

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

        except mExc.MapleTagNotFoundException:

            return None
        
        except Exception as e:

            raise mExc.MapleException(e) from e

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

            except mExc.MapleTagNotFoundException:

                # If the tag does not exist

                tagInd = eInd

            except Exception as e:

                raise mExc.MapleException(e) from e
            
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

        except mExc.MapleDataNotFoundException as dnfe:

            raise mExc.MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise mExc.MapleException(ex) from ex
        
        return True
    #
    ############################
    # Get tag value dictioanry

    def getTagValueDic(self, *headers: str) -> dict[str, str]:

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
        
        except mExc.MapleDataNotFoundException as dnfe:

            raise mExc.MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise mExc.MapleException(ex) from ex
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
        
        except mExc.MapleDataNotFoundException as dnfe:

            raise mExc.MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise mExc.MapleException(ex) from ex
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

        except ValueError or mExc.MapleDataNotFoundException as ve:

            raise mExc.MapleDataNotFoundException(self.fileName) from ve
        
        except Exception as e:

            raise mExc.MapleException(e) from e
        
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

        except mExc.MapleDataNotFoundException as dnfe:

            raise mExc.MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise mExc.MapleException(ex) from ex
        
        return retList

""" * * * * * * * * * * * * * """
"""
ToDo list:

* MapleTree *

- Ignore "CMT" tag as a comment line in MapleTree file.

"""
""" * * * * * * * * * * * * * """
