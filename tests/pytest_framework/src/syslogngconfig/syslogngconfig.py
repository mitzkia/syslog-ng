from src.syslogngconfig.config_renderer import ConfigRenderer
from src.syslogngconfig.driver_file.filesource import FileSource
from src.syslogngconfig.driver_file.filedestination import FileDestination
from src.driverio.fileio import FileIO
from src.syslogngconfig.logpath.logpath import LogPaths
from src.syslogngconfig.globaloptions.globaloptions import GlobalOptions
from src.syslogngctl.syslogngctl import SyslogNgCtl


class SyslogNgConfig(object):
    def __init__(self, syslogngpath, logger_factory, file_register, instance_name):
        syslogngpath.set_syslog_ng_runtime_files(instance_name)
        self.syslog_ng_runtime_files = syslogngpath.get_syslog_ng_runtime_files(instance_name)

        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SyslogNgConfig")
        self.file_register = file_register
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, syslogngpath.runtime_parameters, self.syslog_ng_runtime_files['control_socket_path'])

        self.fileio = FileIO(logger_factory)
        self.syslog_ng_config = {
            "version": syslogngpath.runtime_parameters['syslog_ng_version'],
            "include": ["scl.conf"],
            "module": [],
            "define": {},
            "channel": [],
            "block": [],
            "global_options": {},
            "source_statements": {},
            "parser_statements": [],
            "template_statements": [],
            "rewrite_statements": [],
            "filter_statements": [],
            "destination_statements": {},
            "logpaths": {}
        }
        self.raw_config = ""

    def build_file_based_driver(self, driver_object, root_statement, file_name_prefix, driver_options, existing_statement_id):
        file_source_driver_options = driver_object.get_driver_options(file_name_prefix, driver_options)
        if existing_statement_id:
            driver_object.update_statement_with_driver(root_statement, file_source_driver_options, existing_statement_id)
        else:
            driver_object.create_driver_statement(root_statement, driver_object.statement_id)
            driver_object.update_statement_with_driver(root_statement, file_source_driver_options, driver_object.statement_id)
        return driver_object

    def get_filesource(self, file_name_prefix, driver_options=None, existing_statement_id=None):
        file_source_driver = FileSource(self.logger_factory, self.syslog_ng_config, self.file_register, self.syslog_ng_ctl)
        return self.build_file_based_driver(file_source_driver, "source_statements", file_name_prefix, driver_options, existing_statement_id)

    def get_filedestination(self, file_name_prefix, driver_options=None, existing_statement_id=None):
        file_destination_driver = FileDestination(self.logger_factory, self.syslog_ng_config, self.file_register, self.syslog_ng_ctl)
        return self.build_file_based_driver(file_destination_driver, "destination_statements", file_name_prefix, driver_options, existing_statement_id)

    def create_logpath(self, sources, destinations, flags="flow_control"):
        logpath = LogPaths(self.logger_factory, self.syslog_ng_config, sources, destinations, flags)
        return logpath

    def add_global_options(self, global_options):
        global_options = GlobalOptions(self.logger_factory, self.syslog_ng_config, global_options)
        return global_options

    # Write config helper
    def write_config_content(self, config_path):
        if self.raw_config:
            rendered_config = self.raw_config
        else:
            rendered_config = ConfigRenderer(self.logger_factory, self.syslog_ng_config).syslog_ng_config_content
        self.fileio.write(config_path, rendered_config, re_create_file=True)

    def set_raw_config(self, raw_config):
        self.raw_config = raw_config
