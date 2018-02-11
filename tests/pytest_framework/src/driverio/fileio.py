from colorama import Fore, Back, Style
from src.driverio.filemanager import FileManagerWaitForEvent, File


class FileIO(object):
    def __init__(self, logger_factory=None):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("FileIO")

    def read_file(self, file_path, expected_message_counter=1):
        file_manager = FileManagerWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_creation()
        file_manager.wait_until_number_of_lines(expected_lines=expected_message_counter)
        file_content = file_manager.get_content()
        self.logger.info(
            Fore.BLACK + Back.YELLOW +
            "Content received:" + Style.RESET_ALL +
            "\n>>>From path:[%s]\n" % file_path +
            "\n>>>Content:[%s]" % file_content
            )
        return file_content

    def read_pipe(self, file_path):
        file_manager = FileManagerWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_creation()
        pipe_content = file_manager.get_pipe_content()
        self.logger.info(
            Fore.BLACK + Back.YELLOW +
            "Content received:" + Style.RESET_ALL +
            "\n>>>From path:[%s]\n" % file_path +
            "\n>>>Content:[%s]" % pipe_content
            )
        return pipe_content

    def write(self, file_path, content, open_mode="a+"):
        file_manager = File(self.logger_factory, file_path)
        self.logger.info(
            Fore.BLACK + Back.YELLOW +
            "Content written:" + Style.RESET_ALL +
            "\n>>>From path:[%s]\n" % file_path +
            "\n>>>Content:[%s]" % content
            )
        file_manager.write_content(content=content, open_mode=open_mode)
