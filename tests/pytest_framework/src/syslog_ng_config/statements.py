class Statements(object):
    def __init__(self, logger_factory, syslog_ng_config):
        self.logger = logger_factory.create_logger("ConfigStatements")
        self.syslog_ng_config = syslog_ng_config

    def create_driver_statement(self, root_statement, statement_id):
        self.syslog_ng_config[root_statement].update({statement_id: {}})

    def update_statement_with_driver(self, root_statement, driver_content, statement_id):
        self.syslog_ng_config[root_statement][statement_id].update(driver_content)
