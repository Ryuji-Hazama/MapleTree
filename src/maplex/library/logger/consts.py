
CONFIG_KEY = "MapleLogger"
FUNC = "func"
CONSOLE = "Console"
FILE = "File"
CONSOLE_LOG_LEVEL = "ConsoleLogLevel"
FILE_LOG_LEVEL = "FileLogLevel"
MAX_LOG_SIZE = "MaxLogSize"
FILE_MODE = "FileMode"
CONFIG_FILE = "configFile"
WORKING_DIRECTORY = "WorkingDirectory"
FILE_ENCODING = "FileEncoding"
TIMESTAMP_FORMAT = "TimestampFormat"
ALIGN_WIDTH = "AlignWidth"
GET_LOGGER = "getLogger"
CONSOLE_ALIGN_WIDTH = "consoleAlignWidth"
FILE_ALIGN_WIDTH = "fileAlignWidth"
CONSOLE_FORMAT = "ConsoleFormat"
FILE_FORMAT = "FileFormat"

CALLER_NAME = "CallerName"
PROCESS_ID = "pid"

FILE_FORMAT = '({pid}) {timestamp} [{level}]{func} {callerName}{callerFunc}({callerLine})'
CONSOLE_FORMAT = '[{level}]{func} {callerFunc}({callerLine})'

FILE_MODE_OVERWRITE = 'overwrite'
FILE_MODE_DAILY = 'daily'