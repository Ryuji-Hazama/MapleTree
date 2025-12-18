from pydantic import BaseModel

##################################
# Console output colors BaseModel

class ConsoleColors(BaseModel):

    # Standard colors

    Black: str = "\033[30m"
    Red: str = "\033[31m"
    Green: str = "\033[32m"
    Yellow: str = "\033[33m"
    Blue: str = "\033[34m"
    Magenta: str = "\033[35m"
    LightBlue: str = "\033[36m"
    White: str = "\033[37m"

    # Background colors

    bgBlack: str = "\033[40m"
    bgRed: str = "\033[41m"
    bgGreen: str = "\033[42m"
    bgYellow: str = "\033[43m"
    bgBlue: str = "\033[44m"
    bgMagenta: str = "\033[45m"
    bgLightBlue: str = "\033[46m"
    bgWhite: str = "\033[47m"

    # Bright colors

    bBlack: str = "\033[90m"
    bRed: str = "\033[91m"
    bGreen: str = "\033[92m"
    bYellow: str = "\033[93m"
    bBlue: str = "\033[94m"
    bMagenta: str = "\033[95m"
    bLightBlue: str = "\033[96m"
    bWhite: str = "\033[97m"

    # Other formats

    Bold: str = "\033[1m"
    Underline: str = "\033[4m"
    Reversed: str = "\033[7m"
    Reset: str = "\033[0m"