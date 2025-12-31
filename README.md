# :maple_leaf: MapleX :deciduous_tree:

&nbsp;&nbsp;&nbsp;&nbsp;MapleX is a tool set for Maple file format operations, with logging and console color utilities for Python applications.

&nbsp;&nbsp;&nbsp;&nbsp;***You can install the package from pip with the following command.***

```bash
pip install maplex
```

## Maple File

&nbsp;&nbsp;&nbsp;&nbsp;Maple is a file system that I created when I was a child. It's like a combination of the INI file and the Jason file. I made this format that is easy to read and write for both humans and machines.

### Basic Format

```text
All data before MAPLE\n will be ignored

MAPLE
# Maple data must start with "MAPLE"

*MAPLE_TIME
yyyy/MM/dd HH:mm:ss.fffffff
# Encoded time or optional time in the method parameter

H *STATUS
    # File status
    ADT yyyy/MM/dd HH:mm:ss.fffffff
    RDT yyyy/MM/dd HH:mm:ss.fffffff
    CNT {int}
    H #*
        ADT is the most recent edited time
        RDT is the second most recent edited time (before ADT)
        CNT is the data count (Optional)
    E *#
E
H *Header
    # Headers include '*' are system headers
E
H Data Headers
    H Sub Data Header
        CMT Comments
        # This is also a comment
        Tags Properties
        # Propaties cannot include 'CRLF.'
        Tags2 Properties
        # You cannot use the same tags in a Header except CMT and NTE in H NOTES
        H Sub Data Header
            Tags Propaties
            # You can use the same tag in the child header,
            # which is already used in the parent's header
        E
    E
    H *NOTES NOTES_HEADER
        # Note's header
        NTE {strimg}
        NTE ...
        # Note's main strings for the multi-line data
        # COMMENTS IN THE "*NOTES" BLOCK WILL BE DELETED WHEN SAVE VALUE!
    E
    H #*
        This is a comment block.
        Starts with "H #*"
        and ends with "E *#"
    E *#
E
H Data Headers2
E
# "\nEOF\n" must be needed for all data
EOF

All datas after "\nEOF\n" will be ignored
```

### Data boundary

- Maple data will start with a line `MAPLE\n` and end with `\nEOF\n`.
- Data outside those lines will be ignored.

E.g.:

```text
MAPLE

<MAPLE DATA>

EOF
```

:warning: ***Data outside the Maple data could be lost in the future update***.

### Blocks

- Block starts with `H <Header Name>` and ends with `E`.
- Blocks can be nested.

E.g.:

```text
MAPLE

H FOO
    H BAR
        ...<DATA LINES>
    E
    ...<DATA LINES>
E

EOF
```

### Data Lines

- Each data line has a 'tag' in front of the data.
- The string before the very first white space will be treated as a 'tag', and all the data after the white space will be treated as the data.

E.g.: Store `ANY DATA` with a tag `BAR` inside the `FOO` block

```text
MAPLE

H FOO
    BAR ANY DATA
E

EOF
```

### Notes (Multi-lined Data)

`v2.2.0` or newer

- You can save multi-lined data inside `H *NOTES` block.
- You must specify the header when you save notes value.

E.g.:

```text
MAPLE

H *NOTES NOTES_HEADER
    NTE YOU CAN SAVE
    NTE MULTI-LINED DATA
    NTE INSIDE THIS BLOCK
E

EOF
```

### Comments

`v2.1.0` or newer

#### Comment Line

- `CMT` tag line will be ignored as a comment line.
- A line that starts with `#` is also treated as a comment line.

E.g.:

```text
MAPLE

H DATA
    CMT This is a comment line.
    #TAG This is also a comment line.
    NOTACOMMENT # This cannot be a comment.
E

EOF
```

#### Comment Block

- You can write multi-line comments using a comment block that starts with `H #*` and ends with `E *#`.

E.g.:

```text
MAPLE

H #*
    THIS IS A COMMENT BLOCK
    YOU CAN WRITE
    MULTIPLE LINE COMMENTS
E *#

EOF
```

## MapleTree Class

### `__init__()`

```python
class MapleTree(
    fileName: str,
    tabInd: int = 4,
    encrypt: bool = False,
    key: bytes | None = None,
    createBaseFile: bool = False
)
```

|Property|Required|Value|
|--------|--------|-----|
|**`fileName`**|\*|Maple file name|
|**`tabInd`**||White space count for indents|
|**`encrypt`**||File encryption|
|**`key`**||Encryption key|
|**`createBaseFile`**||Create empty base file|

&nbsp;&nbsp;&nbsp;&nbsp;`__init__` initialize the class and load a Maple file data to the buffer.

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("FileName.mpl")
```

#### Open existing Maple file

&nbsp;&nbsp;&nbsp;&nbsp;`__init__` will open the Maple file and load data to the buffer.

```python
mapleFile = MapleTree("FileName.mpl")
```

#### Change indent size

```python
mapleFile = MapleTree("FileName.mpl", tabInd=4)
mapleFile._saveToFile()
```

&nbsp;&nbsp;&nbsp;&nbsp;This makes the maple file look like

```text
MAPLE

H FOO
    H BAR
        <MAPLE DATA LINES>
    E
    <MAPLE DATA LINES>
E

EOF
```

&nbsp;&nbsp;&nbsp;&nbsp;If you change the `tabInd` value

```python
mapleFile = MapleTree("FileName.mpl", tabInd=2)
mapleFile._saveToFile()
```

&nbsp;&nbsp;&nbsp;&nbsp;This makes the maple file look like

```text
MAPLE

H FOO
  H BAR
    <MAPLE DATA LINES>
  E
  <MAPLE DATA LINES>
E

EOF
```

#### Create a Base File

&nbsp;&nbsp;&nbsp;&nbsp;You can create an empty base file when you initialize the class instance.

```python
mapleFile = MapleTree("NewFile.mpl", createBaseFile=True)
```

&nbsp;&nbsp;&nbsp;&nbsp;This creates an empty Maple file if the file `NewFile.mpl` does not exist.

```text
MAPLE
EOF
```

#### File Data Encryption

&nbsp;&nbsp;&nbsp;&nbsp;If `encrypt=True`, the instance decrypts data when it is read, and encrypts data when it is saved.  
&nbsp;&nbsp;&nbsp;&nbsp;You need to specify the byte key when you use encryption, and the file must be encrypted.

```python
mapleFile = MapleTree("FileName.mpl", encrypt=True, key=key)
```

&nbsp;&nbsp;&nbsp;&nbsp;You can create an encrypted base file with `createBaseFile=True` if the file does not exist.

```python
mapleFile = MapleTree("NewFile.mpl", encrypt=True, key=key, createBaseFile=True)
```

### `readMapleTag()`

```python
def readMapleTag(
    tag: str,
    *headers: str
) -> str
```

|Property|Required|Value|
|--------|--------|-----|
|**`tag`**|\*|Tag to find|
|**`headers`**||Headers contains the tag|

&nbsp;&nbsp;&nbsp;&nbsp;`readMapleTag` returns a data string tagged with the `tag` in `headers` and returns `None` if the tag was not found.

E.g.:

Sample Data (`Sample.mpl`)

```text
MAPLE

H FOO
    H BAR
        TAG1 DATA 1
        TAG2 DATA 2
    E
E

EOF
```

```python
from maplex import MapleTree

mapleFile = MapleTree("Sample.mpl")
mapleData = mapleFile.readMapleTag("TAG1", "FOO", "BAR")

print(mapleData)
# Outputs "DATA 1"
```

### `saveTagLine()`

```python
def saveTagLine(
    tag: str,
    valueStr: str,
    willSave: bool,
    *headers: str
) -> None
```

|Property|Required|Value|
|--------|--------|-----|
|**`tag`**|\*|Target tag|
|**`valueStr`**|\*|Data value (string)|
|**`willSave`**|\*|Save to file flag|
|**`headers`**||Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;`saveTagLine` saves a value with a tag in a header block specified by the parameter.

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl", createBaseFile=True)
mapleFile.saveTagLine("TAG", "VALUE", True, "FOO")

```

&nbsp;&nbsp;&nbsp;&nbsp;This code outputs a file contains:

```text
MAPLE
H FOO
    TAG VALUE
E
EOF
```

#### Update a Buffer Content

&nbsp;&nbsp;&nbsp;&nbsp;If `willSave=False`, the buffer content will be updated, but no update on physical file content.

E.g.:

```python
mapleFile.saveTagLine("TAG", "NEW VALUE", False, "FOO")
```

&nbsp;&nbsp;&nbsp;&nbsp;This code changes the contents on buffer like:

```text
MAPLE
H FOO
    TAG NEW VALUE
E
EOF
```

&nbsp;&nbsp;&nbsp;&nbsp;But the change is **NOT** being saved in the file.

```text
MAPLE
H FOO
    TAG VALUE
E
EOF
```

#### Update and Save Changes

&nbsp;&nbsp;&nbsp;&nbsp;If `willSave=True`, all the changes to the buffer will be saved.

```python
mapleFile.saveTagLine("BAR", "ANOTHER VALUE", True, "FOO")
```

&nbsp;&nbsp;&nbsp;&nbsp;This code changes the contents in the file like:

```text
MAPLE
H FOO
    TAG NEW VALUE
    BAR ANOTHER VALUE
E
EOF
```

#### Create New Block and Tag

&nbsp;&nbsp;&nbsp;&nbsp;If the block and/or the header(s) specified with the parameters do not exist in the data, the function creates the new header block(s) and the tag and saves the value.

```python
mapleFile.saveTagLine("TAZ", "NEW HEADER AND TAG", False, "NEW_HEADER")
```

&nbsp;&nbsp;&nbsp;&nbsp;This code will change the data like:

```text
MAPLE
H FOO
    TAG NEW VALUE
    BAR ANOTHER VALUE
E
H NEW_HEADER
    TAZ NEW HEADER AND TAG
E
EOF
```

### `saveValue()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def saveValue(
    tag: str,
    valueString: any,
    *headers: str,
    **kwargs
) -> bool
```

|Property|Required|Value|
|--------|--------|-----|
|**`tag`**|\*|Tag to delete|
|**`value`**|\*|Value to save|
|**`headers`**||Target headers|
|**`kwargs`**||Keyword arguments|

- Same as `saveTagLine()`
- Set `save=True` to save changes to the file.
  - Default: `save=False`

### `deleteTag()`

```python
def deleteTag(
    delTag: str,
    willSave: bool = False,
    *headers: str
) -> bool
```

|Property|Required|Value|
|--------|--------|-----|
|**`delTag`**|\*|Tag to delete|
|**`willSave`**||Save to file flag|
|**`headers`**||Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;Delete a tag and its value.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    BAR DATA 1
    BAZ DATA 2
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl")
mapleFile.deleteTag("BAR", True, "FOO")
```

&nbsp;&nbsp;&nbsp;&nbsp;The file data will be changed like:

```text
MAPLE

H FOO
    BAZ DATA 2
E

EOF
```

### `deleteValue()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def deleteValue(
    delTag: str,
    *headers: str,
    **kwargs
) -> bool
```

|Property|Required|Value|
|--------|--------|-----|
|**`delTag`**|\*|Tag to delete|
|**`headers`**||Target headers|
|**`kwargs`**||Keyword arguments|

- Same as `deleteTag()`
- Set `save=True` to save changes to the file.
  - Default: `save=False`

### `getTagValueDict()`

```python
getTagValueDic(
    *headers: str
) -> dict[str, str]
```

|Property|Required|Value|
|--------|--------|-----|
|**`headers`**||Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;Get tags and values in the header block specified with the parameter as a `dict`.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    BAR DATA 1
    BAZ DATA 2
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl")
dataDict = mapleFile.getTagValueDict()

print(dataDict)
# Outputs "{'BAR': 'DATA 1', 'BAZ': 'DATA 2'}"
```

### `getTags()`

```python
def getTags(
    *headers: str
) -> list[str]
```

|Property|Required|Value|
|--------|--------|-----|
|**`headers`**||Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;Get the list of the tags in the header block specified with the parameter.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    BAR DATA 1
    BAZ DATA 2
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl")
tagList = mapleFile.getTags()

print(tagList)
# Outputs "['BAR', 'BAZ']"
```

### `deleteHeader()`

```python
def deleteHeader(
    delHead: str,
    willSave: bool = False,
    *Headers: str
) -> bool
```

|Property|Required|Value|
|--------|--------|-----|
|**`delHead`**|\*|Deleting header|
|**`willSave`**||Save to file flag|
|**`Headers`**||Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;This deletes an entire header block and its associated data, including child blocks.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    BAR DATA 1
    H BAZ
        QUX DATA 2
    E
E
H QUUX
    CORGE DATA 3
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleTree = MapleTree("SampleData.mpl")
mapleTree.deleteHeader("FOO", True)
```

&nbsp;&nbsp;&nbsp;&nbsp;This code changes the data like:

```text
MAPLE

H QUUX
    CORGE DATA 3
E

EOF
```

### `removeHeader()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def removeHeader(
    delHead: str,
    *headers: str,
    **kwargs
) -> bool
```

|Property|Required|Value|
|--------|--------|-----|
|**`delHead`**|\*|Deleting header|
|**`headers`**||Target headers|
|**`kwargs`**||Keyword arguments|

- Same as `deleteHeader()`
- Set `save=True` for save data to the file.
  - Default: `save=False`

### `getHeaders()`

```python
def getHeaders(
    *headers: str
) -> list
```

|Property|Required|Value|
|--------|--------|-----|
|**`headers`**||Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;Get the list of the headers in the header block specified with the parameter.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    BAR DATA 1
    H BAZ
        QUX DATA 2
    E
E
H QUUX
    CORGE DATA 3
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleTree = MapleTree("SampleData.mpl")
headerList = mapleTree.getHeaders()

print(headerList)
# Outputs "['FOO', 'QUUX']"
```

### `saveNotes()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def saveNotes(
    noteValues: list[str],
    *headers: str,
    **kwargs
    ) -> None
```

|Property|Required|Value|
|--------|--------|-----|
|**`noteValues`**|\*|Data to save|
|**`headers`**|\*|Target headers|
|**`kwargs`**||Keyword arguments|

&nbsp;&nbsp;&nbsp;&nbsp;The function saves string list as a special notes block value. Set `save=True` to save the changes (Default: `save=False`)

E.g.:

```python
from maplex import MapleTree

mapleTree = MapleTree("SampleData.mpl", createBasaFile=True)
stringList = ["Hello", "there!"]
mapleTree.saveNotes(stringList, "FOO", "BAR", save=True)
```

&nbsp;&nbsp;&nbsp;&nbsp;This code creates a new file contains the following contents:

```text
MAPLE

H FOO
    H *NOTES BAR
        NTE Hello
        NTE there!
    E
E

EOF
```

### `saveNote()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def saveNote(
    noteValues: str,
    *headers: str,
    **kwargs
    ) -> None
```

|Property|Required|Value|
|--------|--------|-----|
|**`noteValues`**|\*|Data to save|
|**`headers`**|\*|Target headers|
|**`kwargs`**||Keyword arguments|

&nbsp;&nbsp;&nbsp;&nbsp;The function saves multi-lined string as a special notes block value. Set `save=True` to save the changes (Default: `save=False`)

E.g.:

```python
from maplex import MapleTree

mapleTree = MapleTree("SampleData.mpl", createBasaFile=True)
dataString = "This is a\nmulti-lined data."
mapleTree.saveNotes(dataString, "FOO", "BAR", save=True)
```

&nbsp;&nbsp;&nbsp;&nbsp;This code creates a new file contains the following contents:

```text
MAPLE

H FOO
    H *NOTES BAR
        NTE This is a
        NTE multi-lined data.
    E
E

EOF
```

### `readNotes()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def readNotes(
    *headers: str
    ) -> list[str]
```

|Property|Required|Value|
|--------|--------|-----|
|**`headers`**|\*|Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;Read note block value which specified by the `headers` and return as a string list.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    H *NOTES BAR
        NTE This is a
        NTE multi-lined data.
    E
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl")
stringList = mapleFile.readNotes("FOO", "BAR")

print(stringList)
# Outputs "['This is a', 'multi-lined data.']"
```

### `readNote()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def readNote(
    *headers: str
    ) -> str
```

|Property|Required|Value|
|--------|--------|-----|
|**`headers`**|\*|Target headers|

&nbsp;&nbsp;&nbsp;&nbsp;Read note block value which specified by the `headers` and return as a string.

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    H *NOTES BAR
        NTE This is a
        NTE multi-lined data.
    E
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl")
dataString = mapleFile.readNote("FOO", "BAR")

print(dataString)
# Outputs "This is a
# multi-lined data"
```

### `deleteNotes()`

&nbsp;&nbsp;&nbsp;&nbsp;`v2.2.0` or newer

```python
def deleteNotes(
    *headers: str
    ) -> bool
```

|Property|Required|Value|
|--------|--------|-----|
|**`headers`**|\*|Target headers|
|**`kwargs`**||Keyword args|

&nbsp;&nbsp;&nbsp;&nbsp;Delete note block which specified by the `headers` and return `True` if it success. Set `save=True` to save the changes (Default: `save=False`)

Sample data: `SampleData.mpl`

```text
MAPLE

H FOO
    H *NOTES BAR
        NTE This is a
        NTE multi-lined data.
    E
E

EOF
```

E.g.:

```python
from maplex import MapleTree

mapleFile = MapleTree("SampleData.mpl")
stringList = mapleFile.deleteNotes("FOO", "BAR", save=True)
```

&nbsp;&nbsp;&nbsp;&nbsp;This code changes the file data like:

```text
MAPLE

H FOO
E

EOF
```

## Logger Class

&nbsp;&nbsp;&nbsp;&nbsp;Logger is a logging object for Python applications. It outputs application logs to log files and to standard output.

### Logger Initialization

```python
    def __init__(
            func: str = "",
            workingDirectory: str | None = None,
            cmdLogLevel: str | None = None,
            fileLogLevel: str | None = None,
            maxLogSize: float | None = None
        ) -> None:
```

|Property|Required|Value|
|--------|--------|-----|
|**`func`**||Primary function name|
|**`workingDirectory`**||Log file output directory|
|**`cmdLogLevel`**||Terminal output log level|
|**`fileLogLevel`**||Log file output log level|
|**`maxLogSize`**||Log file max size (MB)|

&nbsp;&nbsp;&nbsp;&nbsp;The parameter overwrites the settings configured in `config.mpl`.

### Usage

```python
from maplex import Logger

logger = Logger("FunctionName")
logger.Info("Hello there!")
```

This outputs:

```console
[INFO ][FunctionName] <module>(4) Hello there!
```

File output will be:  `log_yyyyMMdd.log`

```log
(PsNo) yyyy-MM-dd HH:mm:ss.fff [INFO ][FunctionName] <module>(4) Hello there!
```

#### Log Level

- `TRACE`
- `DEBUG`
- `INFO`
- `WARN`
- `ERROR`
- `FATAL`

#### ShowError function

&nbsp;&nbsp;&nbsp;&nbsp;This outputs the error logs and stuck trace.

Function:

```python
def ShowError(
    ex: Exception,
    message: str | None = None,
    fatal: bool = False
)
```

|Property|Required|Value|
|--------|--------|-----|
|**`ex`**|\*|Exception|
|**`message`**||Custom error message|
|**`fatal`**||Show error as `FATAL`|

- If `fatal=True`, it outputs log as a `FATAL` log level.

### Settings

- You can configure log settings with `config.mpl`.
- If `config.mpl` does not exist, the instance auto-generates the file.

Auto-generated `config.mpl`:

```text
MAPLE
H *LOG_SETTINGS
    CMD INFO
    FLE INFO
    # TRACE, DEBUG, INFO, WARN,
    # ERROR, FATAL, NONE
    MAX 3
    OUT logs
E
EOF
```

|TAG|Value|
|---|-----|
|**`CMD`**|Console log level|
|**`FLE`**|File log level|
|**`MAX`**|Log file max size (MB)|
|**`OUT`**|Log file output path|

- To disable the log output, set log level to `NONE`.
- You can use a `float` number for the file max size (E.g. `2.5` for `2.5MB`)

## Exceptions

### `class MapleException(Exception)`

&nbsp;&nbsp;&nbsp;&nbsp;This is a basic exception class for MapleTree.

### `class MapleFileNotFoundException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file which specified at the instance initialization was not found.

### `class KeyEmptyException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when `encrypt=True` at the instance initialization, but the key for encryption is missing (`None` or empty).

### `class MapleFileLockedException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the instance tries to open the file, but the other instance has already locked the file.

### `class MapleDataNotFoundException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the data is not found in the file.

### `class MapleHeaderNotFoundException(MapleDataNotFoundException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the header (specified by the user) is not found in the data.

### `class MapleTagNotFoundException(MapleDataNotFoundException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the tag (specified by the user) is not found in the data.

### `class NotAMapleFileException(MapleDataNotFoundException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file is not a Maple file.

- The file without a "MAPLE" line.

### `class InvalidMapleFileFormatException(NotAMapleFileException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file format is an invalid Maple format.

- The file has a "MAPLE" line, but the format is wrong or broken.

### `class MapleFileEmptyException(NotAMapleFileException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the file is empty (No data)

### `class MapleSyntaxException(MapleException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the syntax of the MapleTree function (mostly its parameter) is invalid.

### `class MapleTypeException(MapleSyntaxException)`

&nbsp;&nbsp;&nbsp;&nbsp;This occurs when the user hands the unknown keyword arguments as the `**kwargs` to the MapleTree function.

## Console Colors

### Standard colors

|Key|Value|Color|
|---|-----|-----|
|`Black`|\\033\[30m|Black|
|`Red`|\\033\[31m|Red|
|`Green`|\\033\[32m|Green|
|`Yellow`|\\033\[33m|Yellow|
|`Blue`|\\033\[34m|Blue|
|`Magenta`|\\033\[35m|Magenta|
|`LightBlue`|\\033\[36m|LightBlue|
|`White`|\\033\[37m|White|

### Bright colors

|Key|Value|Color|
|---|-----|-----|
|`bBlack`|\\033\[90m|Black|
|`bRed`|\\033\[91m|Red|
|`bGreen`|\\033\[92m|Green|
|`bYellow`|\\033\[93m|Yellow|
|`bBlue`|\\033\[94m|Blue|
|`bMagenta`|\\033\[95m|Magenta|
|`bLightBlue`|\\033\[96m|LightBlue|
|`bWhite`|\\033\[97m|White|

### Background colors

|Key|Value|Color|
|---|-----|-----|
|`bgBlack`|\\033\[40m|Black|
|`bgRed`|\\033\[41m|Red|
|`bgGreen`|\\033\[42m|Green|
|`bgYellow`|\\033\[43m|Yellow|
|`bgBlue`|\\033\[44m|Blue|
|`bgMagenta`|\\033\[45m|Magenta|
|`bgLightBlue`|\\033\[46m|LightBlue|
|`bgWhite`|\\033\[47m|White|

### Other formats

|Key|Value|Description|
|---|-----|-----------|
|`Bold`|\\033\[1m|Bold text|
|`Underline`|\\033\[4m|Underlined text|
|`Reversed`|\\033\[7m|Reversed colors|
|`Reset`|\\033\[0m|Reset formatting|

## Install maplex :inbox_tray:

### From PyPI

```bash
[python[3] -m] pip install maplex [--break-system-packages]
```

### Manual Installation

1. Download `./dist/maplex-<version>-py3-none-any.whl`
2. Run `[python[3] -m] pip install /path/to/downloaded/maplex-<version>-py3-none-any.whl [--break-system-packages]`

### Build the Package by Yourself

&nbsp;&nbsp;&nbsp;&nbsp;Run `python[3] -m build`  

or

&nbsp;&nbsp;&nbsp;&nbsp;Run `python[3] setup.py sdist bdist_wheel`
