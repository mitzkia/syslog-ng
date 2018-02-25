from src.syslog_ng_config.statements import Statements
from src.common.random import Random


class LogPaths(Statements):
    def __init__(self, logger_factory, syslog_ng_config, sources=None, destinations=None, flags=None):
        Statements.__init__(self, logger_factory, syslog_ng_config)
        self.logger = logger_factory.create_logger("ConfigLogpath")
        self.syslog_ng_config = syslog_ng_config
        self.logpath_uniq_id = Random().get_unique_id()
        self.logpath = {
            "source_statements": [],
            "destination_statements": [],
            "flags": []
        }
        if sources:
            self.add_statements(statement_type="source", statements=sources)
        if destinations:
            self.add_statements(statement_type="destination", statements=destinations)
        if flags:
            self.add_flags(flags)

        self.syslog_ng_config['logpaths'][self.logpath_uniq_id] = self.logpath

    def add_statements(self, statement_type, statements):
        if isinstance(statements, list):
            for statement in statements:
                getattr(self, "add_{}".format(statement_type))(statement)
        else:
            getattr(self, "add_{}".format(statement_type))(statements)

    def add_source(self, source_statement):
        self.logpath['source_statements'].append(source_statement.statement_id)

    def add_destination(self, destination_statement):
        self.logpath['destination_statements'].append(destination_statement.statement_id)

    def add_flags(self, flags):
        self.logpath['flags'].append(flags)
