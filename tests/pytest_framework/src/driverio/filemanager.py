import os
import shutil
import stat
from src.common.blocking import wait_until_true, wait_until_stabilized


class File(object):
    def __init__(self, logger_factory, file_path):
        self.file_path = file_path
        self.logger = logger_factory.create_logger("File")

    def is_file_exist(self):
        return os.path.exists(self.file_path)

    def is_regular_file(self):
        return self.is_file_exist() and stat.S_ISREG(os.stat(self.file_path).st_mode)

    def is_named_pipe(self):
        return self.is_file_exist() and stat.S_ISFIFO(os.stat(self.file_path).st_mode)

    def copy_file(self, destination_path):
        shutil.copyfile(self.file_path, destination_path)

    def move_file(self, destination_path):
        shutil.move(self.file_path, destination_path)

    def delete_file(self):
        if self.is_file_exist():
            os.unlink(self.file_path)
        raise Exception("File does not exist: %s" % self.file_path)

    def get_lines(self):
        if self.is_file_exist():
            with open(self.file_path, 'r') as file_object:
                return len(file_object.readlines())
        raise Exception("File does not exist: %s" % self.file_path)

    def get_size(self):
        if self.is_file_exist():
            return os.stat(self.file_path).st_size
        raise Exception("File does not exist: %s" % self.file_path)

    def get_last_modification_time(self):
        if self.is_file_exist():
            return os.stat(self.file_path).st_mtime
        raise Exception("File does not exist: %s" % self.file_path)

    def get_content(self):
        with open(self.file_path, 'r') as file_object:
            return file_object.read()

    def get_pipe_content(self):
        file_object = os.open(self.file_path, os.O_RDONLY | os.O_NONBLOCK)
        merged_content = ""
        while True:
            try:
                pipe_content = os.read(file_object, 1024)
                if pipe_content:
                    merged_content += pipe_content.decode('utf-8')
                else:
                    self.logger.error("writer closed")
                    break
            except BlockingIOError:
                break
        return merged_content

    def write_content(self, content, open_mode):
        with open(self.file_path, open_mode) as file_object:
            file_object.write(self.normalize_line_endings(content))

    def dump_content(self):
        self.logger.info(self.get_content())

    def is_message_in_file(self, expected_message):
        return expected_message in self.get_content()

    def count_message_in_file(self, expected_message):
        return self.get_content().count(expected_message)

    @staticmethod
    def normalize_line_endings(line):
        if not line.endswith("\n"):
            line += "\n"
        return line

class Dir(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def is_dir_exist(self):
        return os.path.isdir(self.dir_path)

    def delete_dir(self):
        if self.is_dir_exist():
            os.rmdir(self.dir_path)
        raise Exception("Dir does not exist: %s" % self.dir_path)

    def create_dir(self):
        if not self.is_dir_exist():
            os.makedirs(self.dir_path)
        raise Exception("Dir already exist: %s" % self.dir_path)

class FileManagerWaitForEvent(File):
    def __init__(self, logger_factory, file_path):
        super().__init__(logger_factory, file_path)
        self.logger = logger_factory.create_logger("FileManagerWaitForEvent")

    def wait_for_creation(self):
        result_file_creation = wait_until_true(self.is_file_exist, monitoring_time=2)
        self.logger.write_message_based_on_value("File created, file_path: [%s]" % self.file_path, result_file_creation)
        return result_file_creation

    def wait_for_not_change(self):
        result_file_change = wait_until_stabilized(self.get_last_modification_time, monitoring_time=5)
        self.logger.write_message_based_on_value("File stopped changing, file_path: [%s]" % self.file_path, result_file_change)
        return result_file_change

    def wait_until_number_of_lines(self, expected_lines):
        result_lines_arrived = wait_until_true(lambda expected_lines: self.get_lines() == expected_lines, expected_lines, monitoring_time=10)
        self.logger.write_message_based_on_value("Expected number of lines arrived, expected lines: [%s], arrived lines: [%s]" % (expected_lines, self.get_lines()), result_lines_arrived)
        return result_lines_arrived

    def wait_for_message(self, expected_message, expected_occurance=1):
        result_file_creation = self.wait_for_creation()
        result_file_change = self.wait_for_not_change()
        message_occurance = self.count_message_in_file(expected_message)
        self.logger.info("Expected message: [%s]" % expected_message)
        self.logger.info("Actual message occurance: %s, Expected message occurance: %s" % (message_occurance, expected_occurance))
        if message_occurance != expected_occurance:
            self.logger.error("Expected occurance not equals with actual message occurance.\nexpected message:[%s]\nexpected occurance:[%s]\nactual occurance:[%s]" % (expected_message, expected_occurance, message_occurance))
        return result_file_creation and result_file_change and (message_occurance == expected_occurance)
