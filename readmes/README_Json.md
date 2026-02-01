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
|**filePath**|\*|JSON file path|3.0.0|
|**fileEncoding**||File encoding|3.0.0|
|**indent**||Indent size for save as a JSON file|3.0.0|
|**ensureAscii**||Ensure ASCII flag when save to a file|3.0.0|
|**encrypt**||Encryption flag|3.0.0|
|**key**|(\*)|Encryption key|3.0.0|

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
