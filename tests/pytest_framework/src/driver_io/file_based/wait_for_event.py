from src.driver_io.file_based.file import File
from src.common.blocking import wait_until_true
from src.common.bufferio import BufferIO


class FileWaitForEvent(File):
    def __init__(self, logger_factory, file_path):
        super().__init__(logger_factory, file_path)
        self.bufferio = BufferIO()
        self.logger = logger_factory.create_logger("FileWaitForEvent")

    def wait_for_creation(self):
        if not self.file_object:
            result_file_has_created = wait_until_true(self.is_file_exist, monitoring_time=10)
            result_file_has_size = wait_until_true(self.get_size, monitoring_time=10)
            self.logger.write_message_based_on_value("File created, file_path: [{}]".format(self.file_path), result_file_has_created)
            return result_file_has_created and result_file_has_size
        return True

    def is_expected_line_in_buffer(self, expected_lines):
        self.bufferio.buffering_messages(self.read)
        return expected_lines == self.bufferio.buffer.count("\n")

    def is_expected_message_in_buffer(self, expected_message):
        # temp_list = self.bufferio.pop_msgs(self.read)
        self.bufferio.buffering_messages(self.read)
        # return expected_message in temp_list[0]
        result = expected_message in self.bufferio.buffer
        if result:
            self.bufferio.split_buffer_until_message(expected_message)
        return result

    def is_number_of_expected_message_in_buffer(self, expected_message, number_of_expected_message):
        self.bufferio.buffering_messages(self.read)
        return number_of_expected_message == self.bufferio.buffer.count(expected_message)

    def wait_for_number_of_lines(self, expected_lines):
        result_file_creation = self.wait_for_creation()
        found_expected_lines = wait_until_true(self.is_expected_line_in_buffer, expected_lines)
        return result_file_creation and found_expected_lines

    def wait_for_message(self, expected_message):
        result_file_creation = self.wait_for_creation()
        found_expected_message = wait_until_true(self.is_expected_message_in_buffer, expected_message)
        return result_file_creation and found_expected_message

    def wait_for_number_of_expected_message(self, expected_message, number_of_expected_message):
        result_file_creation = self.wait_for_creation()
        found_expected_message = wait_until_true(self.is_number_of_expected_message_in_buffer, expected_message, number_of_expected_message)
        return result_file_creation and found_expected_message
