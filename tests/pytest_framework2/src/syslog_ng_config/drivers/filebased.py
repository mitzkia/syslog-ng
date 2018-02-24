import secrets
from src.syslog_ng_config.config_drivers import Drivers
from src.driver_io.file_based.fileinterface import FileInterface


class FileBasedFactory(Drivers):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        driver_io = FileInterface(logger_factory)
        super().__init__(logger_factory, syslog_ng_config, file_register, driver_io, syslog_ng_ctl)

    def initialize_driver(self, statement_name, statement_short_name, driver_name, mandatory_option):
        self.statement_name = statement_name
        self.statement_short_name = statement_short_name
        self.driver_name = driver_name
        self.mandatory_option = mandatory_option
        self.root_statement = "{}_statements".format(self.statement_name)
        self.driver_type = "{}_{}".format(self.driver_name, self.statement_name)
        self.statement_id = "stmt_id_{}".format(secrets.token_hex(3))
        self.driver_id = "drv_id_{}".format(secrets.token_hex(3))

    def get_statement_id(self):
        return self.statement_id

    def get_driver_id(self):
        return self.driver_id

    def remove_file_source(self):
        self.remove_driver_from_statement(self.root_statement, self.statement_id, self.driver_id)

    def generate_driver_options(self, file_name_prefix, driver_options):
        self.mandatory_option = self.generate_mandatory_option({self.mandatory_option: file_name_prefix},
                                                               driver_type=self.driver_type)
        all_driver_options = self.merge_mandatory_and_driver_options(self.mandatory_option, driver_options)
        self.driver_connection_path = self.mandatory_option[self.mandatory_option]
        driver_content = {
            self.driver_id: {
                "driver_options": all_driver_options,
                "mandatory_option_name": self.mandatory_option,
                "mandatory_option_value": self.mandatory_option[self.mandatory_option],
                "driver_name": self.driver_name
            }
        }
        return driver_content

    def update_driver_options(self, driver_options):
        if driver_options[self.mandatory_option]:
            driver_options[self.mandatory_option] = self.generate_mandatory_option(driver_options, driver_type=self.driver_type)[self.mandatory_option]
            self.mandatory_option[self.mandatory_option] = driver_options[self.mandatory_option]
            self.driver_connection_path = self.mandatory_option[self.mandatory_option]
        self.update_driver_with_options(self.root_statement, self.statement_id, self.driver_id, driver_options)

    def build_file_based_driver(self, file_name_prefix, driver_options, existing_statement_id):
        driver_content = self.generate_driver_options(file_name_prefix, driver_options)
        if existing_statement_id:
            self.update_statement_with_driver(self.root_statement, driver_content, existing_statement_id)
        else:
            self.create_driver_statement(self.root_statement, self.statement_id)
            self.update_statement_with_driver(self.root_statement, driver_content, self.statement_id)


class FileSource(FileBasedFactory):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        super().__init__(logger_factory, syslog_ng_config, file_register, syslog_ng_ctl)
        self.initialize_driver("source", "src", "file", "file_path")

    def write(self, message):
        return self.driver_io.write_content(self.driver_connection_path, content=message)


class FileDestination(FileBasedFactory):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        super().__init__(logger_factory, syslog_ng_config, file_register, syslog_ng_ctl)
        self.initialize_driver("destination", "dst", "file", "file_path")

    def get_expected_output_message(self, message_parts, expected_message_counter=1):
        message_parts = {**message_parts, **{"priority": "skip"}}
        return self.message.construct_bsd_messages(message_parts, expected_message_counter)

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
