import secrets
from src.syslog_ng_config.drivers.drivers import Drivers
from src.driver_io.file_based.interface import FileInterface


class FileBasedFactory(Drivers):
    def __init__(self, logger_factory, syslog_ng_config, file_register, syslog_ng_ctl):
        driver_io = FileInterface(logger_factory)
        Drivers.__init__(self, logger_factory, syslog_ng_config, file_register, driver_io, syslog_ng_ctl)
        self.logger = logger_factory.create_logger("FileBasedFactory")
        self.statement_name = None
        self.statement_short_name = None
        self.driver_name = None
        self.mandatory_option_name = None
        self.root_statement = None
        self.driver_type = None
        self.statement_id = None
        self.driver_id = None
        self.mandatory_option = None
        self.driver_connection_path = None

    def initialize_driver(self, statement_name, statement_short_name, driver_name, mandatory_option_name):
        self.statement_name = statement_name
        self.statement_short_name = statement_short_name
        self.driver_name = driver_name
        self.mandatory_option_name = mandatory_option_name
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
        self.mandatory_option = self.generate_mandatory_option({self.mandatory_option_name: file_name_prefix},
                                                               driver_type=self.driver_type)
        all_driver_options = self.merge_mandatory_and_driver_options(self.mandatory_option, driver_options)
        self.driver_connection_path = self.mandatory_option[self.mandatory_option_name]
        driver_content = {
            self.driver_id: {
                "driver_options": all_driver_options,
                "mandatory_option_name": self.mandatory_option_name,
                "mandatory_option_value": self.mandatory_option[self.mandatory_option_name],
                "driver_name": self.driver_name
            }
        }
        return driver_content

    def update_driver_options(self, driver_options):
        if driver_options[self.mandatory_option_name]:
            driver_options[self.mandatory_option_name] = self.generate_mandatory_option(driver_options, driver_type=self.driver_type)[self.mandatory_option_name]
            self.mandatory_option[self.mandatory_option_name] = driver_options[self.mandatory_option_name]
            self.driver_connection_path = self.mandatory_option[self.mandatory_option_name]
        self.update_driver_with_options(self.root_statement, self.statement_id, self.driver_id, driver_options)

    def build_file_based_driver(self, file_name_prefix, driver_options, existing_statement_id):
        driver_content = self.generate_driver_options(file_name_prefix, driver_options)
        if existing_statement_id:
            self.update_statement_with_driver(self.root_statement, driver_content, existing_statement_id)
        else:
            self.create_driver_statement(self.root_statement, self.statement_id)
            self.update_statement_with_driver(self.root_statement, driver_content, self.statement_id)
