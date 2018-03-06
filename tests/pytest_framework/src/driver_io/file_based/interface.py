from src.driver_io.file_based.file import File
from src.driver_io.file_based.wait_for_event import FileWaitForEvent
# from src.common.bufferio import BufferIO


class FileInterface(object):
    def __init__(self, logger_factory=None):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("FileInterface")

    def read_content(self, file_path, expected_message_counter=1):
        file_manager = FileWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_number_of_lines(expected_message_counter)
        file_content = file_manager.bufferio.buffer
        # file_content = file_manager.bufferio.pop_msgs(file_manager.read)
        self.logger.info(
            "Content received:" +
            "\n>>>From path:[{}]\n".format(file_path) +
            "\n>>>Content:[{}]".format("".join(file_content))
        )
        return "".join(file_content)

    def write_content(self, file_path, content, open_mode="a+", normalize_line_endings=True):
        file_manager = File(self.logger_factory, file_path)
        self.logger.info(
            "Content written:" +
            "\n>>>From path:[{}]\n".format(file_path) +
            "\n>>>Content:[{}]".format(content)
        )
        file_manager.write(content=content, open_mode=open_mode, normalize_line_endings=normalize_line_endings)
