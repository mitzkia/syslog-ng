# vegyuk ki innen a Messageinterface-t es tegyuk oda ahol hasznalkil
from src.message.message_interface import MessageInterface


class Statements(object):
    def __init__(self, logger_factory, syslog_ng_config):
        self.message = MessageInterface(logger_factory)
        self.syslog_ng_config = syslog_ng_config

    def create_driver_statement(self, root_statement, statement_id):
        self.syslog_ng_config[root_statement].update({statement_id: {}})

    def update_statement_with_driver(self, root_statement, driver_content, statement_id):
        self.syslog_ng_config[root_statement][statement_id].update(driver_content)
