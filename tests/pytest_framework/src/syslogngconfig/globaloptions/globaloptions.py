from src.syslogngconfig.config_statements import Statements


class GlobalOptions(Statements):
    def __init__(self, logger_factory, syslog_ng_config, global_options):
        super().__init__(logger_factory, syslog_ng_config)
        self.syslog_ng_config['global_options'].update(global_options)
