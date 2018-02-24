import logging
import sys
from colorlog import ColoredFormatter # kikapcsolhato legyene console esetben


class Logger(logging.Logger):
    def __init__(self, logger_name, report_file, loglevel, use_console_handler=True, use_file_handler=True):
        super().__init__(logger_name, loglevel)
        self.handlers = []
        if use_console_handler:
            self.__set_consolehandler()
        if use_file_handler:
            self.__set_filehandler(file_name=report_file)

    def __set_filehandler(self, file_name=None):
        file_handler = logging.FileHandler(file_name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def __set_consolehandler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter(
            "\n%(log_color)s%(asctime)s - %(name)s - %(levelname)-5s%(reset)s- %(message_log_color)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={
                'message': {
                    'ERROR': 'red',
                    'CRITICAL': 'red'
                }
            },
            style='%'
        )
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def write_message_based_on_value(self, message, value, loglevel=logging.DEBUG):
        pred = value
        message = "{}: [{}]".format(message, pred)
        if pred:
            self.log(loglevel, message)
        else:
            self.error(message)
