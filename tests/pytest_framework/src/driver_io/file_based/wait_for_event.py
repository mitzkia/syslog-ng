import re
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

    # def is_expected_message_in_buffer(self, expected_message):
    #     message_list = self.bufferio.pop_msg(self.read)
    #     r = re.compile(expected_message)
    #     result = len(list(filter(r.match, message_list))) != 0
    #
    #     # if result:
    #     #     self.bufferio.pop_msgs(self.read)
    #     return result

    def is_number_of_expected_messages_in_buffer(self, expected_message, number_of_expected_message):
        self.bufferio.buffering_messages(self.read)
        return number_of_expected_message == self.bufferio.buffer.count(expected_message)

    def wait_for_number_of_lines(self, expected_lines):
        result_file_creation = self.wait_for_creation()
        found_expected_lines = wait_until_true(self.is_expected_line_in_buffer, expected_lines)
        return result_file_creation and found_expected_lines

    # def wait_for_message_in_buffer(self, expected_message):
    #     r = re.compile(expected_message)
    #     while not r.match(self.bufferio.pop_msg(self.read)):
    #         pass
    #     return True

    def wait_for_message_in_buffer(self, expected_message):
        print("AStart wait_for_message_in_buffer")
        print("AExpected message: %s" % expected_message)
        r = re.compile(expected_message)
        found_message_in_buffer = False
        while not found_message_in_buffer:
            a = self.bufferio.pop_msg(self.read)
            b = r.match(a)
            print("Apopped message from buffer: %s" % a)
            print("Amatching result of expected message on popped message: %s" % b)
            if b is not None:
                found_message_in_buffer = True
            print("Afound message: %s" % found_message_in_buffer)
        # import sys
        # sys.exit(1)
        print("AEnd wait_for_message_in_buffer")
        return True
        # while not r.match(self.bufferio.pop_msg(self.read)):
        #     pass
        # return True

    def wait_for_message(self, expected_message):
        # test this function for the following bad conditions: file never created, expected message never arrived
        if not self.wait_for_creation():
            return False
        return wait_until_true(self.wait_for_message_in_buffer, expected_message, monitoring_time=1)

        # r = re.compile(expected_message)
        # while not r.match(self.bufferio.pop_msg(self.read)):
        #     pass
        # return True

    def wait_for_number_of_messages(self, expected_message, number_of_expected_message):
        result_file_creation = self.wait_for_creation()
        found_expected_message = wait_until_true(self.is_number_of_expected_messages_in_buffer, expected_message, number_of_expected_message)
        return result_file_creation and found_expected_message
