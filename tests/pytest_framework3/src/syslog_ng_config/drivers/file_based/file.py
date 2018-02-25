from src.syslog_ng_config.drivers.file_based.file_based_factory import FileBasedFactory
from src.message.interface import MessageInterface


class FileSource(FileBasedFactory):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        FileBasedFactory.__init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl)
        self.initialize_driver("source", "src", "file", "file_path")
        self.logger = logger_factory.create_logger("FileSource")

    def write(self, message, normalize_line_endings=True):
        return self.driver_io.write_content(self.driver_connection_path, content=message, normalize_line_endings=normalize_line_endings)


class FileDestination(FileBasedFactory):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        FileBasedFactory.__init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl)
        self.initialize_driver("destination", "dst", "file", "file_path")
        self.logger = logger_factory.create_logger("FileDestination")
        self.message_interface = MessageInterface(logger_factory)

    def get_expected_output_message(self, message_parts, expected_message_counter=1):
        message_parts = {**message_parts, **{"priority": "skip"}}
        return self.message_interface.construct_bsd_messages(message_parts, expected_message_counter)

    def read(self, expected_message_counter=1):
        return self.driver_io.read_content(self.driver_connection_path,
                                           expected_message_counter=expected_message_counter)

    def read_messages(self, expected_message_counter=2):
        return self.read(expected_message_counter).splitlines(keepends=True)

# class PipeSource(FileBasedFactory):
#     def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
#         super().__init__(logger_factory, syslog_ng_config, file_register, syslog_ng_ctl)
#         self.initialize_driver("source", "src", "pipe")

#     def write(self, message):
#         return self.driver_io.write_content(self.driver_connection_path, content=message, open_mode='w')

# class PipeDestination(FileBasedFactory):
#     def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
#         super().__init__(logger_factory, syslog_ng_config, file_register, syslog_ng_ctl)
#         self.initialize_driver("destination", "dst", "pipe")

#     def get_expected_output_message(self, message_parts, expected_message_counter=1, use_message_counter=True):
#         message_parts = {**message_parts, **{"priority": "skip"}}
#         if expected_message_counter == 1:
#             return self.message.create_bsd_message(defined_bsd_message_parts=message_parts, use_message_counter=use_message_counter)
#         return self.message.create_multiple_bsd_messages(defined_bsd_message_parts=message_parts, message_counter=expected_message_counter, use_message_counter=use_message_counter)

#     def read(self):
#         return self.driver_io.read_pipe(self.driver_connection_path)
