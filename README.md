# :maple_leaf: Maple Tree :deciduous_tree:

&nbsp;&nbsp;&nbsp;&nbsp;MapleTree is a tool set for Maple file, and a logger for the python applications.

## MapleTree

&nbsp;&nbsp;&nbsp;&nbsp;Maple is a file system that I created when I was a child. It's like a combination of the INI file and the Jason file. I created this easy to read and write for both humans and machines.

## Logger

&nbsp;&nbsp;&nbsp;&nbsp;Logger is a logging object for Python applications. It outputs application logs to log files and to standard output.

### Usage

```python
import MapleTree

Logger = MapleTree.Logger("FunctionName")
logger.Info("Hello there!")
```

This outputs:

```console
[INFO ][FunctionName] <module>(7) Hello there!
```

File output will be:  `log_yyyyMMdd.log`

```log
(PsNo) yyyy-MM-dd HH:mm:ss.fff [INFO ][FunctionName] <module>(4) Hello there!
```

#### Log Level

- TRACE
- DEBUG
- INFO
- WARN
- ERROR
- FATAL

#### ShowError function

&nbsp;&nbsp;&nbsp;&nbsp;This outputs the error logs and stuck trace.

Function:

```python
MapleTree.Logger.ShowError(ex: Exception, message: str | None = None, fatal: bool = False)
```

If `fatal=True`, it outputs log as a `FATAL` log level.

### Settings

Working on...

## Install MapleTree :inbox_tray:

1. Download `./dist/MapleTree-<version>-py3-none-any.whl`
2. Run `python[3] -m pip install /path/to/downloaded/MapleTree-<veision>-py3-none-any.whl [--break-system-packages]`

## If You Build Package by Yourself

Run `python[3] -m build`  

or

Run `python[3] setup.py sdist bdist_wheel`
