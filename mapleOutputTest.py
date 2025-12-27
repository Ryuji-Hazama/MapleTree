"""
You can use this file to check the actual output and
Maple file modifications.
"""

import maplex

def runTest():

    try:

        LOG_SETTINGS = "*LOG_SETTINGS"
        CMD = "CMD"
        FLE = "FLE"

        TRACE = "TRACE"
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARN = "WARN"
        ERROR = "ERROR"
        FATAL = "FATAL"

        logger = maplex.Logger("MainLogger")
        config = maplex.MapleTree("config.mpl")
        logger.Info("Starting Maple Output Test")

        # Change log level to TRACE and output all log levels

        config.saveTagLine(CMD, TRACE, False, LOG_SETTINGS)
        config.saveTagLine(FLE, TRACE, True, LOG_SETTINGS)

        loggerOutputAll = maplex.Logger("LoggerOutputAll")
        loggerOutputAll.Trace("This is a TRACE level message.")
        loggerOutputAll.Debug("This is a DEBUG level message.")
        loggerOutputAll.Info("This is an INFO level message.")
        loggerOutputAll.Warn("This is a WARN level message.")
        loggerOutputAll.Error("This is an ERROR level message.")
        loggerOutputAll.Fatal("This is a FATAL level message.")

        # Change console log level to ERROR

        config.saveTagLine(CMD, ERROR, True, LOG_SETTINGS)

        loggerOutputErrorConsole = maplex.Logger("LoggerOutputErrorConsole")
        loggerOutputErrorConsole.Trace("This is a TRACE level message. Should NOT appear on console.")
        loggerOutputErrorConsole.Debug("This is a DEBUG level message. Should NOT appear on console.")
        loggerOutputErrorConsole.Info("This is an INFO level message. Should NOT appear on console.")
        loggerOutputErrorConsole.Warn("This is a WARN level message. Should NOT appear on console.")
        loggerOutputErrorConsole.Error("This is an ERROR level message. Should appear on console.")
        loggerOutputErrorConsole.Fatal("This is a FATAL level message. Should appear on console.")

        # Change file log level to WARN

        config.saveTagLine(CMD, TRACE, False, LOG_SETTINGS)
        config.saveTagLine(FLE, WARN, True, LOG_SETTINGS)

        loggerOutputWarnFile = maplex.Logger("LoggerOutputWarnFile")
        loggerOutputWarnFile.Trace("This is a TRACE level message. Should NOT appear in file.")
        loggerOutputWarnFile.Debug("This is a DEBUG level message. Should NOT appear in file.")
        loggerOutputWarnFile.Info("This is an INFO level message. Should NOT appear in file.")
        loggerOutputWarnFile.Warn("This is a WARN level message. Should appear in file.")
        loggerOutputWarnFile.Error("This is an ERROR level message. Should appear in file.")
        loggerOutputWarnFile.Fatal("This is a FATAL level message. Should appear in file.")

        # Restore original settings

        logger.Info("Restoring original log settings")
        config.saveTagLine(CMD, INFO, False, LOG_SETTINGS)
        config.saveTagLine(FLE, INFO, True, LOG_SETTINGS)

        # Force log level to WARN for both console and file by parameter

        loggerForceLevel = maplex.Logger("LoggerForceLevel", cmdLogLevel=DEBUG, fileLogLevel=ERROR)
        loggerForceLevel.Trace("This is a TRACE level message. Should NOT appear anywhere.")
        loggerForceLevel.Debug("This is a DEBUG level message. Should appear in only console.")
        loggerForceLevel.Info("This is an INFO level message. Should appear in only console.")
        loggerForceLevel.Warn("This is a WARN level message. Should appear in only console.")
        loggerForceLevel.Error("This is an ERROR level message. Should appear in both console and file.")
        loggerForceLevel.Fatal("This is a FATAL level message. Should appear in both console and file.")

        # Show error message and stack trace

        try:

            1 / 0

        except Exception as e:

            logger.ShowError(e, "An exception occurred during division. (Error level message with stack trace)")
            logger.ShowError(e, "An exception occurred during division. (Fatal level message with stack trace)", True)

        logger.Info("Maple Output Test Completed")

    except Exception as e:

        print(f"An error occurred during the Maple Output Test: {e}")

if __name__ == "__main__":
    runTest()