from .config_keys import *
from .defaults import *
from .dict_keys import *

__all__ = [
    "CONFIG_KEY",
    "CONSOLE",
    "FILE",
    "CONSOLE_LOG_LEVEL",
    "FILE_LOG_LEVEL",
    "MAX_LOG_SIZE",
    "FILE_MODE",
    "WORKING_DIRECTORY",
    "FILE_ENCODING",
    "FORMATS",
    "TIMESTAMP",
    "FORMAT",
    "DIGITS",
    "ALIGN_WIDTH",
    "CONSOLE_LOG_FORMAT",
    "FILE_LOG_FORMAT",
    "NAME_SPACES",
    "NAME_SPACE",
    # Dictionary keys for internal use
    "GET_LOGGER",
    "FUNC",
    "CONFIG_FILE",
    "CONSOLE_ALIGN_WIDTH",
    "FILE_ALIGN_WIDTH",
    "CALLER_NAME",
    "PROCESS_ID",
    "PARAM_TIMESTAMP",
    "PARAM_FORMATS",
    "PARAM_CONSOLE_FORMAT",
    "PARAM_FILE_FORMAT",
    # Default values
    "FILE_FORMAT",
    "CONSOLE_FORMAT",
    "TIMESTAMP_FORMAT",
    "MILLISECOND_DIGITS",
    "FILE_MODE_OVERWRITE",
    "FILE_MODE_DAILY",
]