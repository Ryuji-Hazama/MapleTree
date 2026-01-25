"""
You can use this file to check the actual log output and
configuration modification effects of the mapleLogger module.
"""

import src.maplex as maplex

def runTest():

    try:

        LOG_SETTINGS = "MapleLogger"
        CMD = "CMD"
        FLE = "FLE"

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
        logger.log(f"Console log level: {loggerForceLevel.getConsoleLogLevel()}")
        logger.log(f"File log level: {loggerForceLevel.getFileLogLevel()}")
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

        logger.log("Maple Output Test Completed")

    except Exception as e:

        print(f"An error occurred during the Maple Output Test: {e}")

if __name__ == "__main__":
    runTest()