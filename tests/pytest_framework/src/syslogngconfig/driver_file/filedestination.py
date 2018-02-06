import secrets
from src.syslogngconfig.config_drivers import Drivers
from src.driverio.fileio import FileIO


class FileDestination(Drivers):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        driver_io = FileIO(logger_factory)
        super().__init__(logger_factory, syslog_ng_config, file_register, driver_io, syslog_ng_ctl)
        self.statement_name = "destination"
        self.statement_short_name = "dst"
        self.driver_name = "file"
        self.driver_type = "%s_%s" % (self.driver_name, self.statement_name)
        self.statement_id = "stmt_id_%s" % secrets.token_hex(8)
        self.driver_id = "drv_id_%s" % secrets.token_hex(8)
        self.mandatory_option = None
        self.driver_connection_path = None

    def get_driver_options(self, file_name_prefix, driver_options):
        self.mandatory_option = self.generate_mandatory_option({"file_path": file_name_prefix}, driver_type=self.driver_type)
        all_driver_options = self.generate_driver_options(self.mandatory_option, driver_options)
        self.driver_connection_path = self.mandatory_option['file_path']
        file_source_driver_content = {
            self.driver_id: {
                "driver_options": all_driver_options,
                "connection_mandatory_options": self.mandatory_option['file_path'],
                "driver_name": self.driver_name
            }
        }
        return file_source_driver_content

    def update_file_destination_options(self, driver_options):
        if driver_options["file_path"]:
            driver_options["file_path"] = self.generate_mandatory_option(driver_options, driver_type=self.driver_type)["file_path"]
        self.update_driver_with_options("%s_statements" % self.statement_name, self.statement_id, self.driver_id, driver_options)

    def get_statement_id(self):
        return self.statement_id

    def get_driver_id(self):
        return self.driver_id

    def remove_file_source(self):
        self.remove_driver_from_statement("%s_statements" % self.statement_name, self.statement_id, self.driver_id)

    def get_expected_output_message(self, message_parts, expected_message_counter=1):
        message_parts = {**message_parts, **{"priority": "skip"}}
        if expected_message_counter == 1:
            return self.message.create_bsd_message(defined_bsd_message_parts=message_parts, add_newline=True)
        return self.message.create_multiple_bsd_messages(defined_bsd_message_parts=message_parts, message_counter=expected_message_counter, add_newline=True)
