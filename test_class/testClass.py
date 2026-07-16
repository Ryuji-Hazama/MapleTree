import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent))

from src.maplex.mapleLogger import getLogger

class TestLogger:

    def __init__(self):

        self.logger = getLogger(__name__)

    def log_messages(self):

        self.logger.trace("This is a TRACE message.")
        self.logger.debug("This is a DEBUG message.")
        self.logger.info("This is an INFO message.")
        self.logger.warn("This is a WARN message.")
        self.logger.error("This is an ERROR message.")
        self.logger.fatal("This is a FATAL message.")