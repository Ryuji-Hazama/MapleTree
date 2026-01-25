# Logger Class

&nbsp;&nbsp;&nbsp;&nbsp;Logger class is a logging object for Python applications. It outputs application logs to log files and to standard output.

## Logger Initialization

```python
    def __init__(
            func: str = "",
            workingDirectory: str | None = None,
            cmdLogLevel: str | None = None,
            fileLogLevel: str | None = None,
            maxLogSize: float | None = None,
            fileMode: Literal["append", "overwrite", "daily"] | None = None,
            configFile: str = "config.json",
            encoding: str | None = None,
        ) -> None:
```

|Property|Required|Value|Version|
|--------|--------|-----|-------|
|**`func`**||Primary function name||
|**`workingDirectory`**||Log file output directory||
|**`cmdLogLevel`**||Terminal output log level||
|**`fileLogLevel`**||Log file output log level||
|**`maxLogSize`**||Log file max size (MB)||
|**`fileMode`**||Logging file mode|`v3.0`|
|**`configFile`**||Logger configuration file path|`v3.0`|
|**`encoding`**||Log file encoding|`v3.0`|

&nbsp;&nbsp;&nbsp;&nbsp;The parameter overwrites the settings configured in `config.mpl`.

## Usage

```python
from maplex

logger = maplex.getLogger("FunctionName")
logger.info("Hello there!")
```

This outputs:

```console
[INFO ][FunctionName] <module>(4) Hello there!
```

File output will be:  `AppLog.log`

```log
(PsNo) yyyy-MM-dd HH:mm:ss.fff [INFO ][FunctionName] <module>(4) Hello there!
```

### Log Level

- `TRACE`
- `DEBUG`
- `INFO`
- `WARN`
- `ERROR`
- `FATAL`

### ShowError function

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

## Settings

- You can configure log settings with a JSON formatted file (default: `config.json`).
- If the configuration file does not exist, the instance auto-generates the file.
- Instance uses the parameter values to auto-generate a configuration file, or uses the default value if it was not specified.

Auto-generated configuration file (parameters not specified):

```json
{
    "MapleLogger": {
        "ConsoleLogLevel": "INFO",
        "FileLogLevel": "INFO",
        "MaxLogSize": 3.0,
        "WorkingDirectory": "/path/to/output/logs",
        "FileEncoding": "utf-8"
    }
}
```

|Key|Value|
|---|-----|
|**`ConsoleLogLevel`**|Console log level|
|**`FileLogLevel`**|File log level|
|**`MaxLogSize`**|Log file max size (MB)|
|**`WorkingDirectory`**|Log file output path|
|**`FileEncoding`**|Log file encoding|

- To disable the log output, set the log level to `NONE`.
- You can use a `float` number for the file max size (E.g., `2.5` for `2.5MB`)
- You can also use a `str` for the file max size (E.g., `"3M"`)
