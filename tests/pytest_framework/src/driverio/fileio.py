from src.driverio.filemanager import FileManagerWaitForEvent
from colorama import Fore, Back, Style


class FileIO(object):
    def __init__(self, logger_factory=None):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("FileIO")

    def read(self, file_path, expected_message_counter=1):
        file_manager = FileManagerWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_creation()
        file_manager.wait_until_number_of_lines(expected_lines=expected_message_counter)
        file_content = file_manager.get_content()
        self.logger.info(Fore.BLACK + Back.YELLOW +
                        "Content received:" + Style.RESET_ALL +
                        "\n>>>From path:[%s]\n" % file_path +
                        "\n>>>Content:[%s]" % file_content
                        )
        return file_content

    def write(self, file_path, content, append=True):
        if append:
            open_mode = "a+"
        else:
            open_mode = "w"
        self.logger.info(Fore.BLACK + Back.YELLOW +
                         "Content written:" + Style.RESET_ALL +
                         "\n>>>From path:[%s]\n" % file_path +
                         "\n>>>Content:[%s]" % content
                         )
        with open(file_path, open_mode) as file_object:
            file_object.write(self.normalize_line_endings(content))

    @staticmethod
    def normalize_line_endings(line):
        if not line.endswith("\n"):
            line += "\n"
        return line
