import datetime
import json
import os
import base64
from cryptography.fernet import Fernet
from . import mapleExceptions as mExc

class MapleJson:

    """
    MapleJson is a utility class for handling JSON files with optional encryption support. It provides methods to read and write JSON data, as well as manage encryption keys.
    """

    def __init__(self,
                 filePath: str,
                 fileEncoding: str = 'utf-8',
                 indent: int = 4,
                 ensureAscii: bool = False,
                 encrypt: bool = False,
                 key: bytes = None
                 ) -> None:

        """
        Initialize a MapleJson instance.

        :param filePath: Path to the JSON file.
        :param fileEncoding: Encoding of the JSON file.
        :param indent: Indentation level for JSON formatting.
        :param ensureAscii: Whether to ensure ASCII characters in JSON.
        :param encrypt: Whether to encrypt the JSON file.
        :param key: Encryption key for the JSON file.
        """

        self.filePath = filePath
        self.fileEncoding = fileEncoding
        self.indent = indent
        self.ensureAscii = ensureAscii
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

        return self.ensureAscii
    
    def setEnsureAscii(self, ensureAscii: bool) -> None:

        self.ensureAscii = ensureAscii

    def isEncrypted(self) -> bool:

        return self.encrypt
    
    def setEncryption(self, encrypt: bool, key: bytes | None = None) -> None:

        self.encrypt = encrypt

        if encrypt and not key:

            raise mExc.KeyEmptyException(self.filePath)

        self.key = key
        self.fernet = Fernet(key) if encrypt and key else None

    def getKey(self) -> bytes | None:

        return self.key

    def setKey(self, key: bytes) -> None:

        self.key = key
        self.fernet = Fernet(key) if self.encrypt and key else None

    #
    #####################
    # Basic File Operations

    def read(self, *keys: str) -> object | None:

        try:

            with open(self.filePath, 'rb') as file:

                data = file.read()

                if self.encrypt and self.fernet:

                    decryptedData = self.fernet.decrypt(data)
                    jsonData = json.loads(decryptedData.decode(self.fileEncoding))

                else:

                    jsonData = json.loads(data.decode(self.fileEncoding))

            # Navigate through keys if provided

            if keys:

                for jsonKey in keys:

                    if jsonData is None:

                        return None

                    jsonData = jsonData.get(jsonKey, None)

            return jsonData
            
        except FileNotFoundError:

            raise mExc.MapleFileNotFoundException(self.filePath)
        
        except Exception as e:

            raise mExc.MapleException(f"Error reading JSON file: {e}")

    def readOrDefault(self, default: object, *keys: str) -> object:

        result = self.read(*keys)
        return result if result is not None else default
        
    def write(self, data: object, *keys: str) -> None:

        """
        Writes data to the JSON file. If keys are provided, the data will be nested accordingly.

        :param data: The data to write.
        :param keys: Optional keys to nest the data under.
        """

        try:

            if len(keys) > 0:

                # Read existing data to preserve other keys

                existingData = self.read() or {}

                # Navigate to the correct location in the nested structure

                currentLevel = existingData

                for i, jsonKey in enumerate(keys):

                    if i == len(keys) - 1:

                        currentLevel[jsonKey] = data

                    else:

                        if jsonKey not in currentLevel or not isinstance(currentLevel[jsonKey], dict):

                            currentLevel[jsonKey] = {}

                        currentLevel = currentLevel[jsonKey]

                dataToWrite = existingData

            else:

                dataToWrite = data

            jsonData = json.dumps(
                dataToWrite,
                indent=self.indent,
                ensure_ascii=self.ensureAscii,
                default=self.datetimeSerializer
            ).encode(self.fileEncoding)

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

    def datetimeSerializer(self, obj: object) -> str:

        if isinstance(obj, (datetime.datetime, datetime.date)):

            return obj.isoformat()

        raise TypeError(f"Type {type(obj)} not serializable")

    def datetimeDeserializer(self, obj: str) -> datetime.datetime | datetime.date | str:

        try:

            return datetime.datetime.fromisoformat(obj)

        except ValueError:

            try:

                return datetime.date.fromisoformat(obj)

            except ValueError:

                return obj

_json: dict[str, MapleJson] = {}

# Get or create a MapleJson instance

def getMapleJson(filePath: str,
                  fileEncoding: str = 'utf-8',
                  indent: int = 4,
                  ensureAscii: bool = False,
                  encrypt: bool = False,
                  key: bytes = None
                  ) -> MapleJson:

    if filePath not in _json:

        _json[filePath] = MapleJson(filePath,
                                    fileEncoding,
                                    indent,
                                    ensureAscii,
                                    encrypt,
                                    key)

    return _json[filePath]

""" * * * * * * * * * * * * * """
"""
ToDo list:

* Json *

"""
""" * * * * * * * * * * * * * """
