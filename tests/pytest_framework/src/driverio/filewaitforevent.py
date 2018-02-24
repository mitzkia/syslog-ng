from src.driverio.file import File
from src.common.blocking import wait_until_true, wait_until_stabilized


class FileWaitForEvent(File):
    def __init__(self, logger_factory, file_path):
        super().__init__(logger_factory, file_path)
        self.logger = logger_factory.create_logger("FileWaitForEvent")

    def wait_for_creation(self):
        result_file_creation = wait_until_true(self.is_file_exist, monitoring_time=2)
        self.logger.write_message_based_on_value("File created, file_path: [{}]".format(self.file_path), result_file_creation)
        return result_file_creation

    def wait_for_not_change(self):
        result_file_change = wait_until_stabilized(self.get_last_modification_time, monitoring_time=5)
        self.logger.write_message_based_on_value("File stopped changing, file_path: [{}]".format(self.file_path), result_file_change)
        return result_file_change

    def wait_until_number_of_lines(self, expected_lines):
        result_lines_arrived = wait_until_true(lambda expected_lines: self.get_lines() == expected_lines, expected_lines, monitoring_time=10)
        self.logger.write_message_based_on_value("Expected number of lines arrived, expected lines: [{}], arrived lines: [{}]".format(expected_lines, self.get_lines()), result_lines_arrived)
        return result_lines_arrived

    def wait_for_message(self, expected_message, expected_occurance=1):
        result_file_creation = self.wait_for_creation()
        result_file_change = self.wait_for_not_change()
        message_occurance = self.count_message_in_file(expected_message)
        self.logger.info("Expected message: [{}]".format(expected_message))
        self.logger.info("Actual message occurance: {}, Expected message occurance: {}".format(message_occurance, expected_occurance))
        if message_occurance != expected_occurance:
            self.logger.error("Expected occurance not equals with actual message occurance.\nexpected message:[{}]\nexpected occurance:[{}]\nactual occurance:[{}]".format(expected_message, expected_occurance, message_occurance))
        return result_file_creation and result_file_change and (message_occurance == expected_occurance)
