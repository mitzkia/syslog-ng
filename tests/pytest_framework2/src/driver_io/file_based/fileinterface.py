from src.driver_io.file_based.file import File
from src.driver_io.file_based.filewaitforevent import FileWaitForEvent


class FileInterface(object):
    def __init__(self, logger_factory=None):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("FileInterface")

    def read_content(self, file_path, expected_message_counter=1):
        file_manager = FileWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_creation()
        file_manager.wait_until_number_of_lines(expected_lines=expected_message_counter)
        file_content = file_manager.read()
        self.logger.info(
            "Content received:" +
            "\n>>>From path:[{}]\n".format(file_path) +
            "\n>>>Content:[{}]".format(file_content)
        )
        return file_content

    def write_content(self, file_path, content, open_mode="a+"):
        file_manager = File(self.logger_factory, file_path)
        self.logger.info(
            "Content written:" +
            "\n>>>From path:[{}]\n".format(file_path) +
            "\n>>>Content:[{}]".format(content)
        )
        file_manager.write(content=content, open_mode=open_mode)
