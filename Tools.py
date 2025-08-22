from os import path, remove
import os
from shutil import move
import subprocess

##############################
# Remove white space

def removeWhiteSpace(strLine: str) -> str:

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

def getTag(mapleLine: str) -> str:

    if mapleLine == "":
        return ""

    # Remove white space in front and add return at the end

    mapleLine = f"{removeWhiteSpace(mapleLine)}\n"
    strLen = len(mapleLine)

    # Start read tag

    try:

        for ind in range(0, strLen):
        
            if mapleLine[ind] == " " or mapleLine[ind] == "\n" or mapleLine[ind] == "\r":
                break
    
    except Exception as ex:

        print(ex)
        raise

    return mapleLine[:ind]

#
###########################
# Get value

def getValue(mapleLine: str) -> str:

    ind = 0

    # Remove white space in front

    mapleLine = removeWhiteSpace(mapleLine)
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

        print(ex)
        raise

    # logWriter(LogLevel.DEBUG, f"Value: {"".join(valueStrList)}")
    return mapleLine[ind:strLen - 1]

#
#######################
# To MAPLE

def toMaple(readFile, writeFile = None):

    fileLine = readFile.readline()

    while fileLine != "":

        if writeFile != None:

            writeFile.write(fileLine)

        fileLine = removeWhiteSpace(fileLine)
        
        if fileLine == "MAPLE\n":

            return True

        fileLine = readFile.readline()
        
    return False

#
#################################
# ToE

''' - - - - - - - - - - - -*
*                          *
* Read maple file to E tag *
*                          *
* - - - - - - - - - - - -'''

def ToE(mapleFile):

    while True:

        mapleLine = mapleFile.readline()

        if mapleLine == "":
            return

        lineTag = getTag(mapleLine)

        if lineTag == "E" or lineTag == "EOF":
            return
        elif lineTag == "H":
            ToE(mapleFile)

#
#################################
# ToE with W

def ToEwithW(baseFile, copyFile):

    while True:

        mapleLine = baseFile.readline()

        if mapleLine == "":
            return

        copyFile.write(mapleLine)
        lineTag = getTag(mapleLine)

        if lineTag == "E" or lineTag == "EOF":
            return
        elif lineTag == "H":
            ToEwithW(baseFile, copyFile)

#
######################
# Format maple file

def mapleFormatter(originalFile: str, saveFile: str = None) -> bool:

    originalFileR = None
    saveFileTemp = None
    tmpFileName = f"{originalFile}.tmp"
    ind = 0


    ''' - - - - - - - - - -*
    * Format and copy data *
    *     to tmp file      *
    * - - - - - - - - - -'''

    if saveFile == None:
        saveFile = originalFile

    try:

        while path.isfile(tmpFileName):
            
            tmpFileName = f"{originalFile}{ind}.tmp"
            ind += 1

        ind = 0

        originalFileR = open(originalFile, "r")
        saveFileTemp = open(tmpFileName, "w")

        # Move to MAPLE tag

        toMaple(originalFileR, saveFileTemp)

        # Read and format file

        fileLine = originalFileR.readline()

        while fileLine != "":

            fileLine = removeWhiteSpace(fileLine)
            indent = ""

            lineTag = getTag(fileLine)

            if lineTag == "E":
                ind -= 1

            for _ in range(0, ind):
                indent += "    "

            saveFileTemp.write(f"{indent}{fileLine}")

            if lineTag == "H":
                ind += 1

            fileLine = originalFileR.readline()

    except Exception as ex:

        print(ex)
        raise

    finally:
        
        if originalFileR != None:
            originalFileR.close()

        if saveFileTemp != None:
            saveFileTemp.close()


    ''' - - - - - - - - - - -*
    * Move file to save path *
    * - - - - - - - - - - -'''

    try:

        if originalFile == saveFile or path.isfile(saveFile):
            os.remove(saveFile)

        # Move file

        move(tmpFileName, saveFile)
        # logWriter(LogLevel.INFO, f"File formatted: {saveFile}")

    except Exception as ex:

        print(ex)
        raise

    # If the format is wrong

    if ind > 0:

        return False

    # If there are no error

    return True

#
#################################
# Read tag line

''' - - - - - - - - - - - - -*
*                            *
* Read a Maple file tag line *
*                            *
* - - - - - - - - - - - - -'''

def readMapleTag(fileName: str, tag: str, *headers: str) -> str:

    retStr = ""
    mapleFile = None
    ind = 0
    headCount = len(headers)

    try:
        if not path.isfile(fileName):
            
            return ""

        mapleFile = open(fileName, "r")
        deepestInd = 0

        # Serch header

        while ind < headCount:

            fileLine = mapleFile.readline()
            lineTag = getTag(fileLine)

            if lineTag == "H":
                if getValue(fileLine) == headers[ind] or headers[ind] == "*":
                    ind += 1
                    deepestInd = ind
                else:
                    ToE(mapleFile)

            elif lineTag == "E":
                ind -= 1

            elif lineTag == "EOF" or fileLine == "":
                
                return ""

        # Serch tag

        while True:

            fileLine = mapleFile.readline()
            lineTag = getTag(fileLine)

            if lineTag == tag:
                retStr = getValue(fileLine)
                break

            elif lineTag == "EOF" or lineTag == "E" or fileLine == "":
                
                break

        return retStr

    except Exception as ex:

        print(ex)
        raise
    
    finally:
        if mapleFile != None:
            mapleFile.close()

#
###################################################
# Save tag line

def saveTagLine(saveFile: str, tag: str, valueStr: str, *headers: str) -> bool:

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

        if mapleFile != None:
            mapleFile.close()

        if mapleCopyFile != None:
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

        if mapleFile != None:
            mapleFile.close()

        if mapleCopyFile != None:
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

        if mapleFile != None:
            mapleFile.close()

        if mapleCopyFile != None:
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