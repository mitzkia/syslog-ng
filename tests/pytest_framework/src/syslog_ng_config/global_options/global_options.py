from src.syslog_ng_config.statements import Statements


class GlobalOptions(Statements):
    def __init__(self, logger_factory, syslog_ng_config, global_options):
        Statements.__init__(self, logger_factory, syslog_ng_config)
        self.logger = logger_factory.create_logger("ConfigGlobalOptions")
        self.syslog_ng_config['global_options'].update(global_options)
