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
    Italic: str = "\033[3m"
    Underline: str = "\033[4m"
    Reversed: str = "\033[7m"
    Reset: str = "\033[0m"

    def Color256(self, color_code: int) -> str:
        """
        Return the ANSI escape code for a 256-color.

        Parameters:
        color_code (int): The color code (0-255) for the desired color.

        Returns:
        str: The ANSI escape code for the specified 256-color.
        """
        if 0 <= color_code <= 255:
            return f"\033[38;5;{color_code}m"
        else:
            raise ValueError("Color code must be in the range 0-255.")