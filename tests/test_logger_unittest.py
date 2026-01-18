import unittest
import os
import tempfile

from src.maplex import Logger

class TestLogger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a temporary directory for log files."""
        cls.test_log_directory = tempfile.mkdtemp()
        pass

    @classmethod
    def tearDownClass(cls):
        """Delete the temporary directory and its contents."""
        for root, dirs, files in os.walk(cls.test_log_directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(cls.test_log_directory)

    def setUp(self):
        self.logger = Logger("test_logger", workingDirectory=self.test_log_directory)

    def test_trace_logging(self):
        try:
            self.logger.trace("This is a trace message for testing.")
        except Exception as e:
            self.fail(f"Logger.trace raised an exception: {e}")

    def test_info_logging(self):
        try:
            self.logger.info("This is an info message for testing.")
        except Exception as e:
            self.fail(f"Logger.info raised an exception: {e}")

    def test_warning_logging(self):
        try:
            self.logger.warn("This is a warning message for testing.")
        except Exception as e:
            self.fail(f"Logger.warn raised an exception: {e}")

    def test_error_logging(self):
        try:
            self.logger.error("This is an error message for testing.")
        except Exception as e:
            self.fail(f"Logger.error raised an exception: {e}")

    def test_fatal_logging(self):
        try:
            self.logger.fatal("This is a fatal message for testing.")
        except Exception as e:
            self.fail(f"Logger.fatal raised an exception: {e}")

    def test_log_logging(self):
        """Logging at None level which usually should not use."""
        try:
            self.logger.log("This is a log message for testing.")
        except Exception as e:
            self.fail(f"Logger.log raised an exception: {e}")

    def test_show_error(self):
        """Show and log an error message and stack trace."""
        try:
            1 / 0  # Intentional ZeroDivisionError
        except Exception as e:
            try:
                self.logger.ShowError("An error occurred during testing.", e)
            except Exception as log_exception:
                self.fail(f"Logger.showError raised an exception: {log_exception}")

if __name__ == '__main__':
    unittest.main()