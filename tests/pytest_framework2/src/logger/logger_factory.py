import logging
from src.logger.logger import Logger


class LoggerFactory(object):
    def __init__(self, report_file_path, loglevel, use_console_handler=True, use_file_handler=True):
        self.report_file = report_file_path
        self.use_console_handler = use_console_handler
        self.use_file_handler = use_file_handler

        self.string_to_loglevel = {
            "info": logging.INFO,
            "debug": logging.DEBUG,
            "error": logging.ERROR
        }
        try:
            self.log_level = self.string_to_loglevel[loglevel]
        except KeyError:
            raise Exception("Unknown defined loglevel: [{}]".format(loglevel))

    def create_logger(self, logger_name):
        return Logger(
            logger_name,
            self.report_file,
            self.log_level,
            use_console_handler=self.use_console_handler,
            use_file_handler=self.use_file_handler
            )
