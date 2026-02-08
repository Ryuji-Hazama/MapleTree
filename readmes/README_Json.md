# MapleJson Class

&nbsp;&nbsp;&nbsp;&nbsp;MapleJson class is a class library to manage the JSON formatted files.

- You can read a JSON file as a `dict` data.
- You can write the `dict` data into a file as a JSON formatted string
- You can save the data as an encrypted data string.
- You can decrypt the encrypted data.

## Class Initialization

```python

def __init__(
    filePath: str,
    fileEncoding: str = 'utf-8',
    indent: int = 4,
    ensure_ascii: bool = False,
    encrypt: bool = False,
    key: bytes = None
) -> None:
```

|Property|Required|Value|Version|
|--------|--------|-----|-------|
|**`filePath`**|\*|JSON file path|3.0.0|
|**`fileEncoding`**||File encoding|3.0.0|
|**`indent`**||Indent size for save as a JSON file|3.0.0|
|**`ensureAscii`**||Ensure ASCII flag when save to a file|3.0.0|
|**`encrypt`**||Encryption flag|3.0.0|
|**`key`**|(\*)|Encryption key (32 bytes)|3.0.0|

&nbsp;&nbsp;&nbsp;&nbsp;Initialize the class with a file path.

### File encoding

&nbsp;&nbsp;&nbsp;&nbsp;You can set a specific file character encoding. Default: `UTF-8`

&nbsp;&nbsp;&nbsp;&nbsp;E.g.: If you are using `Shift_JIS` (Japanese system), you should initialize the class like the example below:

```python
from maplex import MapleJson

jsonInstance = MapleJson("jsonFile.json", fileEncoding="shift_jis")
```

### Indent size

&nbsp;&nbsp;&nbsp;&nbsp;You can set the block indent size with `indent` parameter. Default: `4`

&nbsp;&nbsp;&nbsp;&nbsp;If you set `indent=2`, the file will be save like the example below:

```json
{
  "Data": {
    "Key": "Value",
  }
}
```

### Ensure ASCII

&nbsp;&nbsp;&nbsp;&nbsp;You can set the flag to ensure ASCII encoding.

&nbsp;&nbsp;&nbsp;&nbsp;If you don't set the parameter (Default: `False`), the file contents after saving are look like the example below:

```json
{
    "data": {
        "japanese": "値",
        "russian": "значение",
        "english": "value"
    }
}
```

&nbsp;&nbsp;&nbsp;&nbsp;But, if you set `ensureAscii=True`, the file contents after saving will be changed like:

```json
{
    "data": {
        "japanese": "\u5024",
        "russian": "\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435",
        "english": "value"
    }
}
```

### Encrypt

&nbsp;&nbsp;&nbsp;&nbsp;If you set `encrypt=True`, set the [encryption key](#key), and save data to a file using the `MapleJson` class, the file will be encrypted with AES-128 (using Fernet).

&nbsp;&nbsp;&nbsp;&nbsp;The encrypted file can be read using the `MapleJson` class, and it is also necessary to set `encrypt=True` and use the same key.

&nbsp;&nbsp;&nbsp;&nbsp;**There is no *redo*** in encryption. **DO NOT FORGET** your encryption key, or *you will lose your data FOREVER.*

### Key

&nbsp;&nbsp;&nbsp;&nbsp;A 32-byte byte-string key for encryption.

&nbsp;&nbsp;&nbsp;&nbsp;If you set `encrypt=True` when initializing the class, you must also set the key.

&nbsp;&nbsp;&nbsp;&nbsp;Encryption example:

```python
from maplex import MapleJson

key = b'Yj6wIw5VR3Z-4nXXdWTZAhwU6j2SIgSQNl7QbYgDyCA='
jsonData = MapleJson("sampleFile.json", encrypt=True, key=key)

sampleData = {
    "setting1": True,
    "setting2": "value2",
    "setting3": 12345
}

jsonData.write(sampleData)
```

&nbsp;&nbsp;&nbsp;&nbsp;Inside the `sampleFile.json` will be:

```text
gAAAAABph_yYxWIyHpS1HImudFoWQQ5WTh2VsPxO4dcXGbYujR62dW1wpZDUf1cZJF-jGzDfTLGHi6e4ihQJRTvNibgIm3sRFLJUyRClRUBSsd1mMmZ0YzFk_ZuinaNSLox3RILZwIMCCE0XbWjw_vs5x_gCKXJQdtEYZ3bSWcSyYBHBAqh3OxA=
```

&nbsp;&nbsp;&nbsp;&nbsp;The you can read the data with:

```python
from maplex import MapleJson

# Set the same key that was used in encryption
key = b'Yj6wIw5VR3Z-4nXXdWTZAhwU6j2SIgSQNl7QbYgDyCA='
jsonData = MapleJson("sampleFile.json", encrypt=True, key=key)
dictFromJson = jsonData.read()

print(dictFromJson)
```

&nbsp;&nbsp;&nbsp;&nbsp;The console output will be:

```text
{'setting1': True, 'setting2': 'value2', 'setting3': 12345}
```

&nbsp;&nbsp;&nbsp;&nbsp;**DO NOT FORGET YOUR ENCRYPTION KEY**,  or you will lose your data *FOREVER.* There is no redo in encryption.

## Functions

### `read()`

```python
def read(
    *keys: str
) -> dict | None:
```

|Property|Required|Value|Version|
|--------|--------|-----|-------|
|**`*keys`**||Dict keys|3.0.0|

&nbsp;&nbsp;&nbsp;&nbsp;This function reads a JSON file, which is specified at the class instance, and returns the data as a `dict` object.

&nbsp;&nbsp;&nbsp;&nbsp;While the data in the `sampleFile.json` is:

```json
{
    "settings": {
        "setting1": True,
        "setting2": "value2",
        "setting3": 12345
    },
    "data": {
        "data1": "value1",
        "data2": 67890
    }
}
```

&nbsp;&nbsp;&nbsp;&nbsp;Read with:

```python
from maplex import MapleJson

jsonFile = MapleJson("sampleFile.json")
jsonData = jsonFile.read()

print(jsonData)
```

&nbsp;&nbsp;&nbsp;&nbsp;The output will be:

```text
{'settings': {'setting1': True, 'setting2': 'value2', 'setting3': 12345}, 'data': {'data1': 'value1', 'data2': 67890}}
```

&nbsp;&nbsp;&nbsp;&nbsp;If you provide the key(s) in the parameter, the function returns the object of the key, and returns `None` if the key does not exist.

```python
from maplex import MapleJson

jsonFile = MapleJson("sampleFile.json")
jsonData = jsonFile.read("data")

print(jsonData)
```

&nbsp;&nbsp;&nbsp;&nbsp;This outputs:

```text
{'data1': 'value1', 'data2': 67890}
```

### `write()`

```python
def write(
    data: dict
) -> None:
```

|Property|Required|Value|Version|
|--------|--------|-----|-------|
|**`data`**|\*|Dict object to save|3.0.0|

&nbsp;&nbsp;&nbsp;&nbsp;This function saves the `dict` object to a file in JSON format.

&nbsp;&nbsp;&nbsp;&nbsp;This overwrites the existing file and creates a new file if the file does not exist.

```python
from maplex import MapleJson

jsonFile = MapleJson("sampleFile")
jsonData = {"data1": True, "data2": "value2", "data3": 12345}
jsonFile.write(jsonData)
```

&nbsp;&nbsp;&nbsp;&nbsp;This creates a file that contains the following data:

```json
{
    "data1": True,
    "data2": "value2",
    "data3": 12345
}
```

&nbsp;&nbsp;&nbsp;&nbsp;The function **overwrites the entire file** with the provided data. So you should be careful, especially when reading with the key(s) and saving their data.

&nbsp;&nbsp;&nbsp;&nbsp;While the data in the `sampleFile.json` is:

```json
{
    "settings": {
        "setting1": True,
        "setting2": "value2",
        "setting3": 12345
    },
    "data": {
        "data1": "value1",
        "data2": 67890
    }
}
```

```python
from maplex import MapleJson

jsonFile = MapleJson("sampleFile.json")
jsonData = jsonFile.read("settings")
jsonFile.write(jsonData)
```

&nbsp;&nbsp;&nbsp;&nbsp;This code changes the file contents like the sample below:

```json
{
    "setting1": True,
    "setting2": "value2",
    "setting3": 12345
}
```

### `generateKey()`

```python
def generateKey(
    setAsCurrent: bool = False
) -> bytes:
```

|Property|Required|Value|Version|
|--------|--------|-----|-------|
|**`setAsCurrent`**||Using the generated key as a current encryption key|3.0.0|

&nbsp;&nbsp;&nbsp;&nbsp;The function returns the randomly generated encryption byte-string key.

- If you set `setAsCurrent=False`, nothing will be changed in the instance state.
- If you set `setAsCurrent=True` while the encryption state was set as `True`, the instance encryption key is overwritten by the newly generated key.
- If you set `setAsCurrent=True` while the encryption state was set as `False`, the instance encryption state is changed to `True` and the newly generated key is set as an encryption key.

&nbsp;&nbsp;&nbsp;&nbsp;E.g. Encrypt a json file:

```python
from maplex import MapleJson

jsonFile = MapleJson("sampleFile.json")
jsonData = jsonFile.read()
key = jsonFile.generateKey(True)
# YOU MUST SAVE THE KEY in the safe storage.
jsonFile.write(jsonData)
```

&nbsp;&nbsp;&nbsp;&nbsp;The code will encrypt the `sampleFile.json` with AES-128 encryption with the randomly generated key.

&nbsp;&nbsp;&nbsp;&nbsp;**There is no *redo*** in encryption. **DO NOT FORGET** your encryption key, or *you will lose your data FOREVER.*

## Getters and Setters

&nbsp;&nbsp;&nbsp;&nbsp;Every class parameter has its own getter and setter functions, and you can set, change, or get those values after initializing the class.

- You need to set the encryption key when you set the encryption to `True`.
