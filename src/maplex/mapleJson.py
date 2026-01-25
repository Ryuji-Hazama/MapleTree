import json
import os
import base64
from cryptography.fernet import Fernet
from . import mapleExceptions as mExc

class MapleJson:

    def __init__(self, filePath: str, fileEncoding: str = 'utf-8', indent: int = 4, ensure_ascii: bool = True, encrypt: bool = False, key: bytes = None):

        self.filePath = filePath
        self.fileEncoding = fileEncoding
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        self.encrypt = encrypt
        self.key = key
        self.fernet = Fernet(key) if encrypt and key else None

    #
    #####################
    # Getter / Setter

    def getFilePath(self) -> str:

        return self.filePath
    
    def setFilePath(self, filePath: str) -> None:

        self.filePath = filePath

    def getFileEncoding(self) -> str:

        return self.fileEncoding
    
    def setFileEncoding(self, fileEncoding: str) -> None:

        self.fileEncoding = fileEncoding

    def getIndent(self) -> int:

        return self.indent
    
    def setIndent(self, indent: int) -> None:

        self.indent = indent

    def getEnsureAscii(self) -> bool:

        return self.ensure_ascii
    
    def setEnsureAscii(self, ensure_ascii: bool) -> None:

        self.ensure_ascii = ensure_ascii

    def isEncrypted(self) -> bool:

        return self.encrypt
    
    def setEncryption(self, encrypt: bool, key=None) -> None:

        self.encrypt = encrypt

        if encrypt and not key:

            raise mExc.KeyEmptyException(self.filePath)

        self.key = key
        self.fernet = Fernet(key) if encrypt and key else None

    def getKey(self) -> bytes:

        return self.key

    def setKey(self, key: bytes) -> None:

        self.key = key
        self.fernet = Fernet(key) if self.encrypt and key else None

    #
    #####################
    # Basic File Operations

    def read(self) -> dict:

        try:

            with open(self.filePath, 'rb') as file:

                data = file.read()

                if self.encrypt and self.fernet:

                    decryptedData = self.fernet.decrypt(data)
                    return json.loads(decryptedData.decode(self.fileEncoding))

                else:

                    return json.loads(data.decode(self.fileEncoding))

        except FileNotFoundError:

            raise mExc.MapleFileNotFoundException(self.filePath)
        
        except Exception as e:

            raise mExc.MapleException(f"Error reading JSON file: {e}")
        
    def write(self, data: dict) -> None:

        try:

            if type(data) is not dict:

                raise mExc.MapleTypeException(self.filePath, "Data to write must be a dictionary")

            jsonData = json.dumps(data, indent=self.indent, ensure_ascii=self.ensure_ascii).encode(self.fileEncoding)

            if self.encrypt and self.fernet:

                encryptedData = self.fernet.encrypt(jsonData)

                with open(self.filePath, 'wb') as file:

                    file.write(encryptedData)

            else:

                with open(self.filePath, 'wb') as file:

                    file.write(jsonData)

        except Exception as e:

            raise mExc.MapleException(f"Error writing JSON file: {e}")

    #
    #####################
    # Utility Methods

    #
    #####################
    # Generate Encryption Key

    def generateKey(self, setAsCurrent: bool = False) -> bytes:

        """
        Generates a new Fernet encryption key.
        Args:
            setAsCurrent (bool): If True, sets the generated key as the current key for the instance.
        Returns:
            bytes: The generated encryption key.
        """

        key = Fernet.generate_key()

        if setAsCurrent:

            self.key = key
            self.fernet = Fernet(key)
            self.encrypt = True

        return key