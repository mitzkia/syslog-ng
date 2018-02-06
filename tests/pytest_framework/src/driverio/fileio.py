from src.driverio.filebasedio import FileBasedIO


class FileIO(FileBasedIO):
    def __init__(self, logger_factory=None):
        super().__init__(logger_factory)
        self.logger = logger_factory.create_logger("FileIO")

    def read(self, file_path, expected_message_counter=1):
        if not self.is_file_exist(file_path):
            self.wait_for_file_creation(file_path)
        self.wait_for_expected_number_of_lines_in_file(file_path=file_path, expected_lines=expected_message_counter)
        return self.get_content_from_regular_file(file_path)

    def write(self, file_path, content, re_create_file=False):
        self.logger.info("SUBSTEP Content write\n>>>ContentIn:[%s]\n>>>to path:[%s]" % (content, file_path))
        if re_create_file:
            self.delete_file(file_path)

        with open(file_path, 'a+') as file_object:
            file_object.write(self.normalize_line_endings(content))
