"""
You can use this file to check the actual log output and
configuration modification effects of the mapleLogger module.
"""

import datetime
import src.maplex as maplex
from test_class.testClass import TestLogger

def runTest():

    try:

        LOG_SETTINGS = "MapleLogger"

        TRACE = "TRACE"
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARN = "WARN"
        ERROR = "ERROR"
        FATAL = "FATAL"
        NONE = "NONE"

        logger = maplex.getLogger(__name__)
        config = maplex.MapleJson("config.json")
        logger.info("Starting Maple Output Test")

        # Color test

        try:

            colors = maplex.ConsoleColors()
            print(f"{colors.Black}This is black text.{colors.Reset}")
            print(f"{colors.Red}This is red text.{colors.Reset}")
            print(f"{colors.Green}This is green text.{colors.Reset}")
            print(f"{colors.Yellow}This is yellow text.{colors.Reset}")
            print(f"{colors.Blue}This is blue text.{colors.Reset}")
            print(f"{colors.Magenta}This is magenta text.{colors.Reset}")
            print(f"{colors.LightBlue}This is light blue text.{colors.Reset}")
            print(f"{colors.White}This is white text.{colors.Reset}")
            print(f"{colors.bgBlack}This is text with black background.{colors.Reset}")
            print(f"{colors.bgRed}This is text with red background.{colors.Reset}")
            print(f"{colors.bgGreen}This is text with green background.{colors.Reset}")
            print(f"{colors.bgYellow}This is text with yellow background.{colors.Reset}")
            print(f"{colors.bgBlue}This is text with blue background.{colors.Reset}")
            print(f"{colors.bgMagenta}This is text with magenta background.{colors.Reset}")
            print(f"{colors.bgLightBlue}This is text with light blue background.{colors.Reset}")
            print(f"{colors.bgWhite}This is text with white background.{colors.Reset}")
            print(f"{colors.bBlack}This is bright black text.{colors.Reset}")
            print(f"{colors.bRed}This is bright red text.{colors.Reset}")
            print(f"{colors.bGreen}This is bright green text.{colors.Reset}")
            print(f"{colors.bYellow}This is bright yellow text.{colors.Reset}")
            print(f"{colors.bBlue}This is bright blue text.{colors.Reset}")
            print(f"{colors.bMagenta}This is bright magenta text.{colors.Reset}")
            print(f"{colors.bLightBlue}This is bright light blue text.{colors.Reset}")
            print(f"{colors.bWhite}This is bright white text.{colors.Reset}")
            print(f"{colors.Bold}This is bold text.{colors.Reset}")
            print(f"{colors.Italic}This is italic text.{colors.Reset}")
            print(f"{colors.Underline}This is underlined text.{colors.Reset}")
            print(f"{colors.Reversed}This is reversed text.{colors.Reset}")

            for i in range(16):
                print(f"{colors.Color256(i)}This is 256-color code {i}.{colors.Reset}")

            i = 16
            for q in range(6):

                j = 0
                k = i

                for r in range(6):

                    print(f"{colors.Color256(k)}{k:03d}{colors.Reset}", end='')
                    k += 6

                print()
                i += 1

                if i == 232:
                    break

            for i in range(232, 256):
                print(f"{colors.Color256(i)}{i:03d}{colors.Reset}", end='')

            print()

        except Exception as e:

            logger.ShowError(e, "An error occurred during the color test.")

        # Change log level to TRACE and output all log levels

        logger.setConsoleLogLevel(TRACE)
        logger.setFileLogLevel(TRACE)
        logger.saveLogSettings()

        logger.log(f"Current Json status: {config.read().get(LOG_SETTINGS, {})}")
        logger.trace("This is a TRACE level message.")
        logger.debug("This is a DEBUG level message.")
        logger.info("This is an INFO level message.")
        logger.warn("This is a WARN level message.")
        logger.error("This is an ERROR level message.")
        logger.fatal("This is a FATAL level message.")
        logger.log("This is a NONE level message, which should not use for logging.")

        # Change console log level to ERROR

        logger.setConsoleLogLevel(ERROR)
        logger.saveLogSettings()

        logger.log(f"Current Json status: {config.read().get(LOG_SETTINGS, {})}")
        logger.trace("This is a TRACE level message. Should NOT appear on console.")
        logger.debug("This is a DEBUG level message. Should NOT appear on console.")
        logger.info("This is an INFO level message. Should NOT appear on console.")
        logger.warn("This is a WARN level message. Should NOT appear on console.")
        logger.error("This is an ERROR level message. Should appear on console.")
        logger.fatal("This is a FATAL level message. Should appear on console.")
        logger.log("This is a NONE level message. Should appear on console.")

        # Change file log level to WARN

        logger.setConsoleLogLevel(TRACE)
        logger.setFileLogLevel(WARN)
        logger.saveLogSettings()

        logger.log(f"Current Json status: {config.read().get(LOG_SETTINGS, {})}")
        logger.trace("This is a TRACE level message. Should NOT appear in file.")
        logger.debug("This is a DEBUG level message. Should NOT appear in file.")
        logger.info("This is an INFO level message. Should NOT appear in file.")
        logger.warn("This is a WARN level message. Should appear in file.")
        logger.error("This is an ERROR level message. Should appear in file.")
        logger.fatal("This is a FATAL level message. Should appear in file.")
        logger.log("This is a NONE level message. Should appear in file.")

        # Restore original settings

        logger.log("Restoring original log settings")
        logger.setConsoleLogLevel("INFO")
        logger.setFileLogLevel("INFO")
        logger.saveLogSettings()

        # Force log level to WARN for both console and file by parameter

        loggerForceLevel = maplex.Logger("LoggerForceLevel", cmdLogLevel=DEBUG, fileLogLevel=ERROR)
        logger.log(f"Current Json status: {config.read().get(LOG_SETTINGS, {})}")
        logger.log(f"Console log level: {loggerForceLevel.getConsoleLogLevel().name}")
        logger.log(f"File log level: {loggerForceLevel.getFileLogLevel().name}")
        loggerForceLevel.trace("This is a TRACE level message. Should NOT appear anywhere.")
        loggerForceLevel.debug("This is a DEBUG level message. Should appear in only console.")
        loggerForceLevel.info("This is an INFO level message. Should appear in only console.")
        loggerForceLevel.warn("This is a WARN level message. Should appear in only console.")
        loggerForceLevel.error("This is an ERROR level message. Should appear in both console and file.")
        loggerForceLevel.fatal("This is a FATAL level message. Should appear in both console and file.")
        loggerForceLevel.log("This is a NONE level message. Should appear in both console and file.")

        # Show error message and stack trace

        try:

            1 / 0

        except Exception as e:

            logger.ShowError(e, "An exception occurred during division. (Error level message with stack trace)")
            logger.ShowError(e, "An exception occurred during division. (Fatal level message with stack trace)", True)

        noFucnLogger = maplex.Logger()
        noFucnLogger.info("This is a log message from a logger without function name.")

        dailyLogger = maplex.getDailyLogger("DailyLoggerTest")
        dailyLogger.info("This is a log message from a daily logger.")

        loggerAlignTest = maplex.Logger("AlignTests1234567890123456", cmdLogLevel=DEBUG, fileLogLevel=DEBUG)
        loggerAlignTest.debug("This is a DEBUG level message to test alignment.")
        loggerAlignTest.info("This is an INFO level message to test alignment.")
        loggerAlignTest.warn("This is a WARN level message to test alignment.")
        loggerAlignTest.error("This is an ERROR level message to test alignment.")
        loggerAlignTest.fatal("This is a FATAL level message to test alignment.")
        loggerAlignTest.log("This is a NONE level message to test alignment.")

        # Namespace specific log level test

        TestLogger().log_messages()

        logger.log("Maple Output Test Completed")

    except Exception as e:

        print(f"An error occurred during the Maple Output Test: {e}")

if __name__ == "__main__":
    runTest()