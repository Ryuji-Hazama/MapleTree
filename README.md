# MapleX

&nbsp;&nbsp;&nbsp;&nbsp;MapleX is a Python library for simple logging, json file operations, Maple file format operations, and console color utilities.

&nbsp;&nbsp;&nbsp;&nbsp;***You can install the package from pip with the following command.***

```bash
pip install MapleX
```

## Logger Class

&nbsp;&nbsp;&nbsp;&nbsp;Logger is a logging object for Python applications. It outputs application logs to log files and to console (standard output).

&nbsp;&nbsp;&nbsp;&nbsp;Easy and simple enough to use, yet highly practical. The best logging library for beginners and for personal projects.

### Beginner Friendly

#### Color Highlited Output

&nbsp;&nbsp;&nbsp;&nbsp;The output will be color-highlighted for better analysis based on the log level. (Not tested on macOS, and you need Windows Terminal for Windows OS)

![Log output sample image](logOutputSample.png)

#### Outputs Stack Trace

&nbsp;&nbsp;&nbsp;&nbsp;You can use a function to outputs error message and the stack trace at once.

![Stack Trace output sample image](logErrorOutputSample.png)

### Logger Sample

```python
import maplex

logger = maplex.getLogger("FunctionName")
logger.info("Hello there!")
```

This outputs to console:

```console
[INFO ][FunctionName] <module>(4) Hello there!
```

Also outputs to the log file:

```log
(PsNo) yyyy-MM-dd HH:mm:ss.fff [INFO ][FunctionName] <module>(4) Hello there!
```

[More details](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_Logger.md)

[Logging Tips](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/LoggingTips.md)

## MapleJson

&nbsp;&nbsp;&nbsp;&nbsp;MapleJson class is a library class for convert data between `dict` data and JSON formatted file data.

&nbsp;&nbsp;&nbsp;&nbsp;You can read, write and also encrypt a JSON file as a `dict` data.

[More details](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_Json.md)

## Maple File Format

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
            # which is already used in the parents' header
        E
    E
    H *NOTES NOTES_HEADER
        # Note's header
        NTE {strimg}
        NTE ...
        # Notes' main strings for the multi-line data
        # COMMENTS IN THE "*NOTES" BLOCK WILL BE DELETED WHEN SAVING!
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

[More details](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_MapleTree.md#maple-file)

## MapleTree Class

&nbsp;&nbsp;&nbsp;&nbsp;MapleTree class is a Python library for read, edit, and write the Maple formatted file from the Python code.  
&nbsp;&nbsp;&nbsp;&nbsp;You can also automatically encrypt the file data using the library functions.

[More details](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_MapleTree.md#mapletree-class)

## Exceptions

&nbsp;&nbsp;&nbsp;&nbsp;Excption classes are the specialized classes for MapleX to make your debug easier.

[More details](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_Exceptions.md#exceptions)

## Console Colors

&nbsp;&nbsp;&nbsp;&nbsp;ConsoleColors class is a class library for color-highlight the standard output.

[More details](https://github.com/Ryuji-Hazama/MapleTree/blob/main/readmes/README_ConsoleColors.md)

## Install MapleX

### From PyPI

```bash
[python[3] -m] pip install MapleX [--break-system-packages]
```

### Manual Installation

1. Download `./dist/maplex-<version>-py3-none-any.whl`
2. Run `[python[3] -m] pip install /path/to/downloaded/maplex-<version>-py3-none-any.whl [--break-system-packages]`

### Build the Package by Yourself

&nbsp;&nbsp;&nbsp;&nbsp;Run `python[3] -m build`  

or

&nbsp;&nbsp;&nbsp;&nbsp;Run `python[3] setup.py sdist bdist_wheel`

### Unit test

```bash
python[3] -m unittest discover -s tests
```
