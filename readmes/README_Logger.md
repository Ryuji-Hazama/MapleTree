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

## Functions

### `getLogger()`

```python
def getLogger(
    name = "",
    **kwargs
) -> maplex.Logger:
```

|Property|Required|Value|Version|
|--------|--------|-----|-------|
|**`name`**||Primary funcion name|`v3.0`|
|**`**kwargs`**||Other parameters|`v3.0`|

&nbsp;&nbsp;&nbsp;&nbsp;This get or creates a Logger instance.

&nbsp;&nbsp;&nbsp;&nbsp;If you already have a Logger class instance with the same name, the function returns the existing instance, and you can save your resources on the machine.

```python
from maplex

logger = maplex.getLogger(__name__)
```

## Getters and Setters

&nbsp;&nbsp;&nbsp;&nbsp;Every class parameter has its own getter and setter functions, and you can set, change, or get those values after initializing the class.

## Logging Methods

```python
def trace(object: any) -> None:
def debug(object: any) -> None:
def info(object: any) -> None:
def warn(object: any) -> None:
def error(object: any, exception: Exception | None = None) -> None:
def fatal(object: any, exception: Exception | None = None) -> None:
```

- You can use `exception` parameter to log the exception details along with a custom message in `error` and `fatal` methods in `v3.2.0` or later.

&nbsp;&nbsp;&nbsp;&nbsp;Each function outputs the log in each log level.

## `ShowError` Function

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
        "MaxLogSize": 3,
        "WorkingDirectory": "logs",
        "FileEncoding": "utf-8",
        "Formats": {
            "Timestamp": {
                "Format": "%F %X.%f",
                "Digits": null
            },
            "ConsoleLogFormat": "[{level}]{func} {callerFunc}{callerLine}",
            "FileLogFormat": "({pid}) {timestamp} [{level}]{func} {callerName}{callerFunc}({callerLine})",
            "Separator": ": "
        }
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
|**`Formats`**|Log format settings|
|**`NameSpaces`**|Namespace specific log level settings|

- To disable the log output, set the log level to `NONE`.
- You can use a `float` number for the file max size (E.g., `2.5` for `2.5MB`)
- You can also use a `str` for the file max size (E.g., `"3M"`)
- You can set the timestamp format with the `Format` key in the `Timestamp` section of the `Formats` settings.
  - The default format is `%F %X.%f`, which outputs the timestamp as `yyyy-MM-dd HH:mm:ss.fff`. You can use any valid Python datetime format string.
- You can set the number of digits for the timestamp with the `Digits` key in the `Timestamp` section of the `Formats` settings.

### Formats

&nbsp;&nbsp;&nbsp;&nbsp;`v3.2.0` or later

- You can set the log format for console and file output with the `ConsoleLogFormat` and `FileLogFormat` keys in the `Formats` settings.
- Also, you can set the timestamp format with the `Format` key in the `Timestamp` section of the `Formats` settings.

```json
{
    "MapleLogger": {
        "Formats": {
            "Timestamp": {
                "Format": "%F %X.%f",
                "Digits": -3
            },
            "ConsoleLogFormat": "[{level}]{func} {callerFunc}{callerLine}",
            "FileLogFormat": "({pid}) {timestamp} [{level}]{func} {callerName}{callerFunc}({callerLine})",
            "Separator": ": "
        }
    }
}
```

|Key|Value|
|---|-----|
|**`Timestamp.Format`**|Timestamp format string|
|**`Timestamp.Digits`**|Number of digits for the timestamp|
|**`ConsoleLogFormat`**|Console log format string|
|**`FileLogFormat`**|File log format string|
|**`Separator`**|Separator string between prefix and message|

- You can use standard Python datetime format strings for the `Timestamp.Format` key. For example, `%F %X.%f` outputs the timestamp as `yyyy-MM-dd HH:mm:ss.fff`.
- You can set the number of digits for the timestamp with the `Timestamp.Digits` key.
  - The default value is `null`, which outputs the full length of the timestamp.
  - However, I recommend using `-3` to output the timestamp with milliseconds, which is the most common format for logging.
  - You can use a negative number to specify the number of digits to output from the end of the timestamp. For example, `-3` cuts the last three digits of the timestamp, which outputs the timestamp as `yyyy-MM-dd HH:mm:ss.fff`.
- You can use the following placeholders in the log format strings:

`{pid}`: Process ID  
`{timestamp}`: Timestamp  
`{level}`: Log level  
`{func}`: Function name  
`{callerName}`: Caller function name  
`{callerFunc}`: Caller function name (with module name)  
`{callerLine}`: Caller line number

### Namespace Specific Log Level Settings

- You can set the log level for specific namespaces by adding a `NameSpaces` key in the configuration file.
- The `NameSpaces` key is a list of dictionaries, where each dictionary contains a `NameSpace`, a `ConsoleLogLevel`, and a `FileLogLevel`.

Example:

```json
{
    "MapleLogger": {
        "ConsoleLogLevel": "INFO",
        "FileLogLevel": "INFO",
        "NameSpaces": [
            {
                "NameSpace": "MyNamespace",
                "ConsoleLogLevel": "DEBUG",
                "FileLogLevel": "INFO"
            }
        ]
    }
}
```

- In this example, the log level for the `MyNamespace` namespace is set to `DEBUG` for console output and `INFO` for file output. All other namespaces will use the default log levels specified in the `ConsoleLogLevel` and `FileLogLevel` keys.
- You can use this setting to control the log output for different parts of your application, allowing you to have more detailed logs for specific namespaces while keeping the overall log output at a higher level.
