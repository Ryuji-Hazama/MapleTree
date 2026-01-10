import os.path as path
from cryptography.fernet import Fernet
from . import mapleExceptions as mExc
import warnings

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

        if createBaseFile and not path.isfile(fileName):

            # Create a base Maple file

            try:

                mapleBaseString = "MAPLE\nEOF"

                if encrypt:

                    # Encrypt data

                    mapleBaseString = Fernet(key).encrypt(mapleBaseString.encode()).decode()

                with open(fileName, "w") as f:

                    f.write(mapleBaseString)

            except Exception as e:

                raise mExc.MapleException(e) from e

        try:

            with open(fileName, "r") as f:

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

            # If the file is empty

            if len(self.fileStream) == 0:

                raise mExc.MapleFileEmptyException(fileName)

            # Search data region

            try:

                self.mapleIndex = self.fileStream.index("MAPLE\n")

            except ValueError as ve:

                raise mExc.NotAMapleFileException(fileName) from ve
            
            # Find EOF index

            self.eofIndex = len(self.fileStream) - 1
            self.eofIndex = self._findEof(self.mapleIndex)

            # Check data format

            self._mapleFormatter()
            
        except mExc.MapleFileEmptyException:

            raise

        except FileNotFoundError as fnfe:

            raise mExc.MapleFileNotFoundException(fileName) from fnfe
        
        except mExc.NotAMapleFileException as ve:

            raise mExc.NotAMapleFileException(fileName) from ve

        except Exception as ex:

            raise mExc.MapleException(ex) from ex
        
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
        """
        Save current file stream to file
        """

        # Create file data

        try:

            if self.ENCRYPT:

                fileData = self.__encryptData()

            else:

                fileData = "".join(self.fileStream)

            # Save to file

            with open(self.fileName, "w") as f:

                f.writelines(fileData)

        except Exception as e:

            raise mExc.MapleException(e) from e
        
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

        listLen = len(self.fileStream) - 1

        while startInd < listLen:

            startInd += 1
            lineTag = self.__getTag(self.fileStream[startInd])

            if lineTag == "H":

                # Check for comment block

                lineValue = self.__getValue(self.fileStream[startInd])

                if lineValue[:2] == "#*":

                    # Skip comment block

                    startInd = self.__ToCommentEnd(startInd)
            
            elif lineTag == "EOF":

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
            mapleLine = self.fileStream[curInd]
            mapleTag = self.__getTag(mapleLine)

            if mapleTag == "E":

                return curInd
            
            elif mapleTag == "H":

                # Check for comment block

                lineValue = self.__getValue(mapleLine)

                if lineValue[:2] == "#*":

                    # Skip comment block

                    curInd = self.__ToCommentEnd(curInd)

                else:

                    # Skip to its E

                    curInd = self.__ToE(curInd)

        raise mExc.InvalidMapleFileFormatException(self.fileName)
    
    def __ToCommentEnd(self, curInd: int) -> int:

        """Return comment block end line index of current level
        Raise if not found"""

        while curInd < self.eofIndex:

            curInd += 1
            mapleLine = self.__removeWhiteSpace(self.fileStream[curInd]).rstrip()

            if mapleLine == "E *#":

                return curInd

        raise mExc.InvalidMapleFileFormatException(self.fileName)

    #
    ######################
    # Format maple file

    def _mapleFormatter(self, willSave: bool = False):

        """Format Maple stream
        and save to file if willSave is True"""

        try:

            ind = 0
            i = self.mapleIndex

            # Format

            while i <= len(self.fileStream) - 1:

                mapleLine = self.__removeWhiteSpace(self.fileStream[i])
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

                    if self.__getValue(mapleLine)[:2] == "#*":

                        # Comment block

                        i = self.__ToCommentEnd(i)

                    else:
                        
                        ind += 1

                i += 1

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
        lineIndex = self.mapleIndex
        eInd = self.eofIndex

        if "#*" in headers:

            # Cannot search inside comment block

            headerIndex = headers.index("#*")
            raise mExc.MapleSyntaxException(f"Cannot search inside comment block: Comment block header \"#*\" found in search headers list at index {headerIndex}")

        if len(headers) == 0:

            # Return root block (No headers provided)
            return True, self.eofIndex, self.mapleIndex

        # Find header

        try:

            while lineIndex < eInd:

                mapleLine = self.fileStream[lineIndex]
                mapleTag = self.__getTag(mapleLine)

                if mapleTag == "H":

                    lineValue = self.__getValue(mapleLine)

                    if lineValue[:2] == "#*":

                        # Comment block

                        lineIndex = self.__ToCommentEnd(lineIndex)

                    elif lineValue == headers[ind]:

                        if ind == headCount - 1:

                            headInd = lineIndex
                            eInd = self.__ToE(headInd)
                            
                            return True, eInd, headInd

                        ind += 1

                    else:

                        # Skip to E

                        lineIndex = self.__ToE(lineIndex)

                elif mapleTag == "E":

                    if ind <= 0:

                        raise mExc.InvalidMapleFileFormatException(self.fileName)
                    
                    return False, lineIndex, ind

                lineIndex += 1

        except mExc.InvalidMapleFileFormatException:

            raise

        except Exception as e:
        
            raise mExc.MapleException(e) from e

        return False, eInd, ind
    
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

    def readMapleTag(self, tag: str, *headers: str) -> str | None:

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
    ###############################
    # Save tag line (easier to write)

    def saveValue(self, tag: str, value: any, *headers: str, **kwargs) -> None:

        """Save valueStr to tag in headers.\n
        If the headers does not exist, create new headers.\n
        Overwrte file if save == True"""

        willSave = kwargs.get('save', False)
        self.saveTagLine(tag, f"{value}", willSave, *headers)
    #
    ###################################################
    # Save tag line (out of support)

    def saveTagLine(self, tag: str, valueStr: str, willSave: bool, *headers: str) -> None:

        """(Out of support)\n
        Save valueStr to tag in headers.\n
        If the headers does not exist, create new headers.\n
        Overwrte file if sillSave == True"""

        warnings.warn("saveTagLine is out of support. Use saveValue instead.", DeprecationWarning)

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
    # Delete tag line (easier to write)

    def deleteValue(self, delTag: str, *headers: str, **kwargs) -> bool:

        """
        Delete tag(delTag) from header(headers) in Maple file(delFile)\n
        Return True if it success.
        """

        willSave = kwargs.get('save', False)
        return self.deleteTag(delTag, willSave, *headers)

    #
    #############################
    # Delete tag line (out of support)

    def deleteTag(self, delTag: str, willSave: bool = False, *headers: str) -> bool:

        """(Out of support)\n
        Delete tag(delTag) from header(headers) in Maple file(delFile)\n
        Return True if it success.
        """

        warnings.warn("deleteTag is out of support. Use deleteValue instead.", DeprecationWarning)

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

                    headerValue = self.__getValue(self.fileStream[headInd])

                    if headerValue[:2] == "#*":

                        # Skip comment block

                        headInd = self.__ToCommentEnd(headInd)

                    else:

                        headInd = self.__ToE(headInd)

                elif lineTag == "CMT" or lineTag[0] == "#":

                    # Ignore comment line

                    continue

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

                    headerValue = self.__getValue(self.fileStream[headInd])

                    if headerValue[:2] == "#*":

                        # Skip comment block

                        headInd = self.__ToCommentEnd(headInd)
                    
                    else:

                        headInd = self.__ToE(headInd)

                elif lineTag == "CMT" or lineTag[0] == "#":

                    # Ignore comment line

                    continue

                else:

                    retList.append(lineTag)

            return retList
        
        except mExc.MapleDataNotFoundException as dnfe:

            raise mExc.MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise mExc.MapleException(ex) from ex

    #
    #############################
    # Save notes

    def saveNotes(self, noteValues: list[str], *headers: str, **kwargs) -> None:

        """
        Save note values list to headers in Maple file
        Overwrite existing note block
        """

        if len(headers) == 0:

            raise mExc.MapleSyntaxException("No headers provided to save notes")
        
        willSave = kwargs.get('save', False)
        headersList = list(headers)
        headersLastIndex = len(headersList) - 1
        headersList[headersLastIndex] = f"*NOTES {headersList[headersLastIndex]}"

        try:

            isFound, eInd, headInd = self._findHeader(headersList)

            if not isFound:

                # Create new headers

                headLen = len(headersList)

                while headInd < headLen:

                    self.fileStream.insert(eInd, f"H {headersList[headInd]}\n")
                    eInd += 1
                    self.fileStream.insert(eInd, "E\n")
                    headInd += 1

            else:

                # Delete existing note block

                self.fileStream = self.fileStream[:headInd + 1] + self.fileStream[eInd:]
                eInd = headInd + 1

            # Insert note values

            for noteValue in noteValues:

                self.fileStream.insert(eInd, f"NTE {noteValue}\n")
                eInd += 1

            # Refresh EOF index

            self.eofIndex = self._findEof(headInd + 1)

            # Save?

            self._mapleFormatter(willSave)

        except mExc.MapleException:

            raise

        except Exception as ex:

            raise mExc.MapleException(ex) from ex

    #
    #############################
    # Save note

    def saveNote(self, noteValue: str, *headers: str, **kwargs) -> None:

        """
        Save note value to headers in Maple file
        Overwrite existing note block
        """

        noteValues = noteValue.split("\n")
        self.saveNotes(noteValues, *headers, **kwargs)

    #
    #############################
    # Get notes list

    def readNotes(self, *headers: str) -> list[str]:

        """
        Read note values list from headers in Maple file
        """

        if len(headers) == 0:

            raise mExc.MapleSyntaxException("No headers provided to read notes")
        
        headersList = list(headers)
        headersLastIndex = len(headersList) - 1
        headersList[headersLastIndex] = f"*NOTES {headersList[headersLastIndex]}"

        try:

            isFound, eInd, headInd = self._findHeader(headersList)

            if not isFound:

                self.__headerNotFoundExceptionHandler(headInd, headersList)

            noteValues = []

            for line in self.fileStream[headInd + 1:eInd]:

                lineTag = self.__getTag(line)

                if lineTag == "H":

                    # Note block cannot contain other headers

                    raise mExc.InvalidMapleFileFormatException(self.fileName, "Note block contains other headers")

                elif lineTag == "NTE":

                    noteValues.append(self.__getValue(line))

                else:

                    # Ignore other tags

                    continue

            return noteValues
        
        except mExc.MapleDataNotFoundException as dnfe:

            raise mExc.MapleDataNotFoundException(self.fileName) from dnfe
        
        except Exception as ex:

            raise mExc.MapleException(ex) from ex

    #
    #############################
    # Read notes value

    def readNote(self, *headers: str) -> str:

        """
        Read note value from headers in Maple file
        """

        if len(headers) == 0:

            raise mExc.MapleSyntaxException("No headers provided to read note")
        
        notesList = self.readNotes(*headers)
        return "\n".join(notesList)
    
    #
    #############################
    # Delete notes

    def deleteNotes(self, *headers: str, **kwargs) -> bool:

        """
        Delete note block from headers in Maple file
        Return True if it success.
        """

        if len(headers) == 0:

            raise mExc.MapleSyntaxException("No headers provided to delete notes")

        willSave = kwargs.get('save', False)
        
        headersList = list(headers)
        headersLastIndex = len(headersList) - 1
        headersList[headersLastIndex] = f"*NOTES {headersList[headersLastIndex]}"

        return self.deleteHeader(headersList[-1], willSave, *headersList[:-1])
    
    #
    #############################
    # Delete header (easier to write)

    def removeHeader(self, delHead: str, *headers: str, **kwargs) -> bool:

        """
        Delete header(delHead) from headers in Maple file(delFile)\n
        Return True if it success.
        """

        willSave = kwargs.get('save', False)
        return self.deleteHeader(delHead, willSave, *headers)

    #
    #############################
    # Delete header (out of support)

    def deleteHeader(self, delHead: str, willSave: bool = False, *Headers: str) -> bool:

        """(Out of support)\n"""

        warnings.warn("deleteHeader is out of support. Use removeHeader instead.", DeprecationWarning)

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

    def getHeaders(self, *headers: str) -> list[str]:

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

                    headerValue = self.__getValue(fileLine)

                    if headerValue[:2] == "#*":

                        # Skip comment block

                        headInd = self.__ToCommentEnd(headInd)
                    
                    else:

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

"""
""" * * * * * * * * * * * * * """
