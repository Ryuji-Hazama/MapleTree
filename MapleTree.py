from os import path, remove
import os
from shutil import move
import subprocess
import uuid

################################
# Exception classes

class MapleException(Exception):

    """Basic exception for all exception inside the Maple tree."""

class MapleFileNotFoundException(MapleException):

    def __init__(self, mapleFile: str = "", message: str = "Mapel file not found"):

        self.message = f"{message}: {mapleFile}"
        super().__init__(self.message)

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

    def __init__(self, fileName: str, tabInd: int = 4):

        self.TAB_FORMAT = " " * tabInd
        self.fileName = fileName

        f = None
        
        try:

            f = open(fileName, "r")
            self.fileStream = f.readlines()
            f.close()

            # If the file is only one line or empty

            if len(self.fileStream) < 2:

                raise MapleFileEmptyException(fileName)
            
            # Search data region

            self.mapleIndex = self.fileStream.index("MAPLE\n")

            try:

                self.eofIndex = self.fileStream.index("EOF\n", self.mapleIndex)

            except:

                self.eofIndex = self.fileStream.index("EOF", self.mapleIndex)

            # Check data format

            self.mapleFormatter()
            
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
    # Save to file

    #    
    ##############################
    # Remove white space

    def removeWhiteSpace(self, strLine: str) -> str:

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

    def getTag(self, mapleLine: str) -> str:

        """Get a tag from a data line."""

        if mapleLine == "":
            return ""

        # Remove white space in front and add return at the end

        mapleLine = f"{self.removeWhiteSpace(mapleLine)}\n"
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

    def getValue(self, mapleLine: str) -> str:

        """Get a value from a data line."""

        ind = 0

        # Remove white space in front

        mapleLine = self.removeWhiteSpace(mapleLine)
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
    #######################
    # To MAPLE

    def toMaple(self) -> int:

        """Return line index of \"MAPLE\\n\""""

        return self.mapleIndex

    #
    #################################
    # ToE

    def ToE(self, curInd: int) -> int:

        """Return E tag line index of current level
        Raise"""

        while curInd < self.eofIndex:

            curInd += 1
            mapleLine = self.fileStream[curInd]

            if mapleLine == "E\n":

                return curInd
            
            if self.getTag(mapleLine) == "H":

                curInd = self.ToE(curInd)

        raise InvalidMapleFileFormatException

    #
    ######################
    # Format maple file

    def mapleFormatter(self, willSave: bool = False):

        """Format Maple stream
        and save to file if willSave is True"""

        try:

            ind = 0

            # Format

            for i, mapleLine in enumerate(self.fileStream, self.mapleIndex):

                mapleLine = self.removeWhiteSpace(mapleLine)
                tag = self.getTag(mapleLine)

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

            f = None

            try:

                f = open(self.fileName, "w")
                f.writelines(self.fileStream)
                f.close()

            except Exception as e:

                raise MapleException(e) from e
            
            finally:

                if f is not None:
                    f.close()

    #
    #################################
    # Read tag line

    def readMapleTag(self, tag: str, *headers: str) -> str:

        '''Read a Maple file tag line in headers'''

        ind = 0
        headCount = len(headers)
        headInd = self.mapleIndex
        eInd = self.eofIndex

        # Find header

        try:

            while ind < headCount:

                header = f"{self.TAB_FORMAT * ind}H {headers[ind]}"
                ind += 1
                headInd = self.fileStream.index(header, headInd, eInd)
                eInd = self.ToE(headInd)

        except ValueError:

            if ind < 1:

                raise MapleHeaderNotFoundException(self.fileName, headers[ind])
            
            else:

                raise MapleHeaderNotFoundException(self.fileName, headers[ind], headers[ind - 1])

        except Exception as e:
        
            raise MapleException from e
        
        # Find tag

        ind = headInd

        try:
                
            while ind < eInd:

                ind += 1
                fileLine = self.removeWhiteSpace(self.fileStream[headInd])
                
                if fileLine.startswith(f"{tag} "):

                    return self.getValue(fileLine)
                
                elif fileLine.startswith("H "):

                    ind = self.ToE(ind)

            raise MapleTagNotFoundException

        except MapleTagNotFoundException:

            raise MapleTagNotFoundException(self.fileName, tag, headers[len(headers) - 1])
        
        except Exception as e:

            raise MapleException(e) from e

    # Rewriting here
    ###################################################
    # Save tag line

    def saveTagLine(self, tag: str, valueStr: str, *headers: str) -> None:

        mapleFile = None
        mapleCopyFile = None
        ind = 0
        headCount = len(headers)
        EorEOF = ""

        ''' - - - - - - - - - - - - - - -*
        * Copy file to tmp file and save *
        * - - - - - - - - - - - - - - -'''

        try:
            
            if not path.isfile(saveFile):
                
                return False

            # Create copy file name

            mapleCopyFileName = f"{saveFile}.tmp"

            while path.isfile(mapleCopyFileName):
                mapleCopyFileName = f"{saveFile}{ind}.tmp"
                ind += 1

            # Open files

            ind = 0
            mapleFile = open(saveFile, "r")
            mapleCopyFile = open(mapleCopyFileName, "w")

            # Serch save headers

            while ind < headCount:

                fileLine = mapleFile.readline()
                lineTag = getTag(fileLine)

                if lineTag == "H":

                    mapleCopyFile.write(fileLine)

                    if getValue(fileLine) == headers[ind] or headers[ind] == "*":
                        ind += 1
                    else:
                        ToEwithW(mapleFile, mapleCopyFile)

                elif lineTag == "E" or lineTag == "EOF":

                    EorEOF = fileLine

                    break

                else:

                    mapleCopyFile.write(fileLine)

            # Add headers

            eCount = 0

            while ind < headCount:

                mapleCopyFile.write(f"H {headers[ind]}\n")
                ind += 1
                eCount += 1

            # Serch tag

            if EorEOF == "":

                while True:

                    fileLine = mapleFile.readline()
                    lineTag = getTag(fileLine)

                    if lineTag == tag:
                        break

                    elif lineTag == "E" or lineTag == "EOF":
                        EorEOF = fileLine
                        break

                    else:

                        mapleCopyFile.write(fileLine)

                        if lineTag == "H":
                            ToEwithW(mapleFile, mapleCopyFile)

            # Save line

            mapleCopyFile.write(f"{tag} {valueStr}")

            while eCount > 0:
                mapleCopyFile.write("\nE")
                eCount -= 1

            mapleCopyFile.write(f"\n{EorEOF}")

            # Copy till the end

            fileLine = mapleFile.readline()

            while fileLine != "":
                mapleCopyFile.write(fileLine)
                fileLine = mapleFile.readline()

        except Exception as ex:

            print(ex)
            raise

        finally:

            if mapleFile is not None:
                mapleFile.close()

            if mapleCopyFile is not None:
                mapleCopyFile.close()


        ''' - - - - - - - - - - - - -*
        * Format and copy saved data *
        *     to original file       *
        * - - - - - - - - - - - - -'''

        mapleFormatter(mapleCopyFileName, saveFile)
        remove(mapleCopyFileName)

        return True

    #
    #############################
    # Delete tag line

    def deleteTag(delFile: str, delTag: str, *headers: str) -> bool:

        """
        Delete tag(delTag) from header(headers) in Maple file(delFile)
        Return True if it success.
        """

        mapleFile = None
        mapleCopyFile = None

        try:

            if not path.isfile(delFile):

                return False
            
            # Create tmp file name

            delCopyFile = f"{delFile}.tmp"
            ind = 0

            while path.isfile(delCopyFile):

                delCopyFile = f"{delFile}{ind}.tmp"
                int += 1

            mapleFile = open(delFile, "r")
            mapleCopyFile = open(delCopyFile, "w")

            # Move to MAPLE tag

            toMaple(mapleFile, mapleCopyFile)

            # Dig into headers

            ind = 0

            while ind < len(headers):

                fileLine = mapleFile.readline()
                mapleCopyFile.write(fileLine)
                lineTag = getTag(fileLine)

                if lineTag == "H":

                    lineValue = getValue(fileLine)

                    if lineValue == headers[ind]:

                        ind += 1
                        deepestInd = ind

                    else:

                        ToEwithW(mapleFile, mapleCopyFile)

                elif lineTag == "E":

                    ind -= 1

                elif lineTag == "EOF":

                    return False
            
            # Search tag

            while True:

                fileLine = mapleFile.readline()
                lineTag = getTag(fileLine)

                if lineTag == delTag:

                    break

                elif lineTag == "E" or lineTag == "EOF" or fileLine == "":

                    return False
                
                else:

                    mapleCopyFile.write(fileLine)

            # Copy to the end

            fileLine = mapleFile.readline()

            while fileLine != "":

                mapleCopyFile.write(fileLine)
                fileLine = mapleFile.readline()

            mapleFile.close()
            mapleCopyFile.close()

            # Format file

            mapleFormatter(delCopyFile, delFile)

            return True

        except Exception as ex:

            print(ex)
            raise

        finally:

            if mapleFile is not None:
                mapleFile.close()

            if mapleCopyFile is not None:
                mapleCopyFile.close()

            if path.isfile(delCopyFile):
                remove(delCopyFile)

    #
    #############################
    # Delete header

    def deleteHeader(delFile: str, delHead: str, *Headers: str) -> bool:

        mapleFile = None
        mapleCopyFile = None
        ind = 0

        try:

            if not path.isfile(delFile):

                return False

            # Create tmp file name

            delCopyFile = f"{delFile}.tmp"

            while path.isfile(delCopyFile):

                delCopyFile = f"{delFile}{ind}.tmp"
                ind += 1

            mapleFile = open(delFile, "r")
            mapleCopyFile = open(delCopyFile, "w")
            ind = 0

            # Move to MAPLE tag

            toMaple(mapleFile, mapleCopyFile)

            # Dig into headers

            while ind < len(Headers):

                fileLine = mapleFile.readline()
                mapleCopyFile.write(fileLine)
                lineTag = getTag(fileLine)

                if lineTag == "H":

                    lineValue = getValue(fileLine)

                    if lineValue == Headers[ind]:

                        ind += 1
                        deepestInd = ind

                    else:

                        ToEwithW(mapleFile, mapleCopyFile)

                elif lineTag == "E":

                    ind -= 1

                elif lineTag == "EOF":

                    return False

            # Serch delete header

            fileLine = mapleFile.readline()

            while fileLine != "":

                lineTag = getTag(fileLine)

                if lineTag == "H":

                    lineValue = getValue(fileLine)

                    if lineValue == delHead:

                        # Delete header

                        ToE(mapleFile)
                        break

                    else:

                        mapleCopyFile.write(fileLine)
                        ToEwithW(mapleFile, mapleCopyFile)

                else:

                    mapleCopyFile.write(fileLine)

                    if lineTag == "EOF" or lineTag == "E":

                        return False

                fileLine = mapleFile.readline()

            # Copy to the end

            fileLine = mapleFile.readline()

            while fileLine != "":

                mapleCopyFile.write(fileLine)
                fileLine = mapleFile.readline()

            mapleFile.close()
            mapleCopyFile.close()

            # Format file

            mapleFormatter(delCopyFile, delFile)

            return True

        except Exception as ex:

            print(ex)
            raise

        finally:

            if mapleFile is not None:
                mapleFile.close()

            if mapleCopyFile is not None:
                mapleCopyFile.close()

            if path.isfile(delCopyFile):
                remove(delCopyFile)

    #
    ############################
    # Get headers list

    def getHeaders(readFile: str, *headers: str) -> list[str]:

        """
        Get and return headers list from headers in Maple file(readFile)
        """

        retList = []
        headCount = len(headers)
        i = 0
        f = None

        try:

            f = open(readFile)

            while headCount > i:

                fileLine = f.readline()
                tag = getTag(fileLine)

                if tag == "H":

                    val = getValue(fileLine)

                    if val == headers[i]:

                        i += 1

                    else:

                        ToE(f)

                elif tag == "E":

                    i -= 1

                elif tag == "EOF":

                    return retList
                
            tag = ""
                
            while tag not in {"E", "EOF"}:

                fileLine = f.readline()
                tag = getTag(fileLine)

                if tag == "H":

                    retList.append(getValue(fileLine))
                    ToE(f)

        except Exception as ex:

            print(ex)
            raise

        finally:

            if f is not None:

                f.close()

        return retList

    #
    ############################
    # Get tag list

    def getTags(readFile: str, *headers: str) -> list[str]:

        """
        Get and return tag list from headers in Maple file(readFile)
        """

        retList = []
        headCount = len(headers)
        i = 0
        f = None

        try:

            f = open(readFile)

            while headCount > i:

                fileLine = f.readline()
                tag = getTag(fileLine)

                if tag == "H":

                    val = getValue(fileLine)

                    if val == headers[i]:

                        i += 1

                    else:

                        ToE(f)

                elif tag == "E":

                    i -= 1

                elif tag == "EOF":

                    return retList
                
            tag = ""
                
            while tag not in {"E", "EOF"}:

                fileLine = f.readline()
                tag = getTag(fileLine)

                if tag == "H":

                    ToE(f)

                elif tag not in {"E", "EOF"}:

                    retList.append(tag)

        except Exception as ex:

            print(ex)
            raise

        finally:

            if f is not None:

                f.close()

        return retList

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