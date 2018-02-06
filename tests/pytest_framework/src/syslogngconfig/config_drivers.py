from src.syslogngconfig.config_statements import Statements


class Drivers(Statements):
    def __init__(self, logger_factory, syslog_ng_config, file_register, driver_io, syslog_ng_ctl):
        super().__init__(logger_factory, syslog_ng_config)
        self.file_register = file_register
        self.driver_io = driver_io
        self.syslog_ng_ctl = syslog_ng_ctl

    def generate_mandatory_option(self, mandatory_option, driver_type):
        if "file_path" in mandatory_option.keys():
            if not mandatory_option['file_path']:
                return {"file_path": self.file_register.get_registered_file_path(prefix=driver_type)}
            else:
                return {"file_path": self.file_register.get_registered_file_path(prefix=mandatory_option['file_path'])}

    def generate_driver_options(self, mandatory_option, driver_options):
        if not driver_options:
            driver_options = {}
        return {**mandatory_option, **driver_options}

    def update_driver_with_options(self, root_statement, statement_id, driver_id, driver_options):
        self.syslog_ng_config[root_statement][statement_id][driver_id]['driver_options'].update(driver_options)

    def remove_driver_from_statement(self, root_statement, statement_id, driver_id):
        self.syslog_ng_config[root_statement][statement_id].pop(driver_id)

    def read(self, expected_message_counter=1):
        return self.driver_io.read(self.driver_connection_path, expected_message_counter=expected_message_counter)

    def read_messages(self, expected_message_counter=2):
        return self.driver_io.read(self.driver_connection_path, expected_message_counter=expected_message_counter).splitlines(keepends=True)

    def write(self, message="test message"):
        self.driver_io.write(self.driver_connection_path, content=message)

    def get_query(self):
        exit_code, stdout, stderr = self.syslog_ng_ctl.query(pattern="*%s.%s.%s*" % (self.statement_short_name, self.driver_name, self.statement_id))
        statistical_elements = ["memory_usage", "written", "processed", "dropped", "queued", "stamp"]
        result = {}
        for stat_element in statistical_elements:
            for line in stdout.splitlines():
                if stat_element in line:
                    result.update({stat_element: int(line.split(".")[-1].split("=")[-1])})
        return result
