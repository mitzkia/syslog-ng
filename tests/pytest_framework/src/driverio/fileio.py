from src.driverio.filemanager import FileManagerWaitForEvent


class FileIO(object):
    def __init__(self, logger_factory=None):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("FileIO")

    def read(self, file_path, expected_message_counter=1):
        file_manager = FileManagerWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_creation()
        file_manager.wait_until_number_of_lines(expected_lines=expected_message_counter)
        return file_manager.get_content()

    def write(self, file_path, content, append=True):
        if append:
            open_mode = "a+"
        else:
            open_mode = "w"
        self.logger.info("SUBSTEP Content write\n>>>ContentIn:[%s]\n>>>to path:[%s]" % (content, file_path))
        with open(file_path, open_mode) as file_object:
            file_object.write(self.normalize_line_endings(content))

    @staticmethod
    def normalize_line_endings(line):
        if not line.endswith("\n"):
            line += "\n"
        return line
