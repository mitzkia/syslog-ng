import glob
import os
import shutil
import stat


class File(object):
    def __init__(self, logger_factory, file_path):
        self.file_path = file_path
        self.logger = logger_factory.create_logger("File")
        self.file_object = None

    def is_file_exist(self):
        return os.path.exists(self.file_path)

    def is_wildcard_file_exist(self):
        return glob.glob(self.file_path)

    def is_regular_file(self):
        return stat.S_ISREG(os.stat(self.file_path).st_mode)

    def is_named_pipe(self):
        return stat.S_ISFIFO(os.stat(self.file_path).st_mode)

    def copy_file(self, destination_path):
        return shutil.copyfile(self.file_path, destination_path)

    def move_file(self, destination_path):
        return shutil.move(self.file_path, destination_path)

    def delete_file(self):
        return os.unlink(self.file_path)

    def get_lines(self):
        with open(self.file_path, 'r') as file_object:
            return file_object.read().count("\n")

    def get_size(self):
        return os.stat(self.file_path).st_size

    def get_last_modification_time(self):
        return os.stat(self.file_path).st_mtime

    # def read(self):
    #     if not self.file_object:
    #         self.file_object = open(self.file_path, 'r')
    #     return self.file_object.readline()

    def read(self):
        if not self.file_object:
            self.file_object = open(self.file_path, 'r')
        return self.file_object.read()

    def write(self, content, open_mode, normalize_line_endings):
        with open(self.file_path, open_mode) as file_object:
            if normalize_line_endings:
                file_object.write(self.normalize_line_endings(content))
            else:
                file_object.write(content)

    def dump_content(self):
        self.logger.info(self.read())

    def is_message_in_file(self, expected_message):
        return expected_message in self.read()

    def count_message_in_file(self, expected_message):
        return self.read().count(expected_message)

    @staticmethod
    def normalize_line_endings(line):
        if not line.endswith("\n"):
            line += "\n"
        return line

    def get_files_by_pattern(self):
        return glob.glob(os.path.join(os.getcwd(), self.file_path))
