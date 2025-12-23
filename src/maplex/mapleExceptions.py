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

        if message != "":

            if fileName != "":

                self.message = f"{message}: {fileName}"

            else:

                self.message = message
        
        else:

            self.message = f"Data not found: {fileName}"

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

class NotAMapleFileException(MapleDataNotFoundException):

    def __init__(self, filePath: str = "", message: str = "The file is not a Maple file"):

        self.message = f"{message}: {filePath}"
        super().__init__(self.message)

class InvalidMapleFileFormatException(NotAMapleFileException):

    def __init__(self, mapleFile = "", message = "Invalid Maple file format"):

        self.message = f"[{message}: {mapleFile}]"
        super().__init__(self.message)

class MapleFileEmptyException(NotAMapleFileException):

    def __init__(self, mapleFile="", message="File is empty"):
        super().__init__(mapleFile, message)

class MapleSyntaxException(MapleException):

    def __init__(self, message: str = "Maple syntax error"):

        self.message = message
        super().__init__(self.message)

class MapleTypeException(MapleSyntaxException):

    def __init__(self, mapleFunction: str = "", unexpectedKeywordArg: str = "", message: str = ""):
    
        if message == "":

            self.message = f"Unexpected keyword argument [{unexpectedKeywordArg}] in function [{mapleFunction}]"

        else:

            self.message = message

        super().__init__(self.message)
