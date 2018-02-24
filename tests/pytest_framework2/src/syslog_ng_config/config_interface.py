from src.syslog_ng_config.config_renderer import ConfigRenderer
from src.syslog_ng_config.drivers.filebased import FileSource, FileDestination
from src.syslog_ng_config.logpath.logpath import LogPaths
from src.syslog_ng_config.globaloptions.globaloptions import GlobalOptions
from src.syslog_ng_ctl.syslogngctl import SyslogNgCtl
from src.driver_io.file_based.fileinterface import FileInterface
from src.executor.executor_interface import ExecutorInterface


class ConfigInterface(object):
    def __init__(self, logger_factory, syslog_ng_parameters_object, file_register, instance_name):
        self.logger_factory = logger_factory
        self.file_register = file_register
        self.instance_parameters = syslog_ng_parameters_object.set_instance_parameters(instance_name)
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, self.instance_parameters)
        self.fileinterface = FileInterface(logger_factory)

        self.syslog_ng_config = {
            "version": self.get_syslog_ng_version(),
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

    def get_syslog_ng_version(self):
        syslog_ng_binary_path = self.instance_parameters['binary_file_paths']['syslog_ng_binary']
        executor = ExecutorInterface(self.logger_factory)
        get_version_command = [syslog_ng_binary_path, "--version"]
        version_output = executor.execute_command(command=get_version_command)[1]
        for version_output_line in version_output.splitlines():
            if "Config version:" in version_output_line:
                return version_output_line.split()[2]
        raise Exception("Can not parse 'Config version' from ./syslog-ng --version")

    def get_filesource(self, file_name_prefix, driver_options=None, existing_statement_id=None):
        file_source_driver = FileSource(self.logger_factory, self.syslog_ng_config, self.file_register, self.syslog_ng_ctl)
        file_source_driver.build_file_based_driver(file_name_prefix, driver_options, existing_statement_id)
        return file_source_driver

    def get_filedestination(self, file_name_prefix, driver_options=None, existing_statement_id=None):
        file_destination_driver = FileDestination(self.logger_factory, self.syslog_ng_config, self.file_register, self.syslog_ng_ctl)
        file_destination_driver.build_file_based_driver(file_name_prefix, driver_options, existing_statement_id)
        return file_destination_driver

    # def get_pipesource(self, file_name_prefix, driver_options=None, existing_statement_id=None):
    #     pipe_source_driver = PipeSource(self.logger_factory, self.syslog_ng_config, self.file_register, self.syslog_ng_ctl)
    #     pipe_source_driver.build_file_based_driver(file_name_prefix, driver_options, existing_statement_id)
    #     return pipe_source_driver

    # def get_pipedestination(self, file_name_prefix, driver_options=None, existing_statement_id=None):
    #     pipe_destination_driver = PipeDestination(self.logger_factory, self.syslog_ng_config, self.file_register, self.syslog_ng_ctl)
    #     pipe_destination_driver.build_file_based_driver(file_name_prefix, driver_options, existing_statement_id)
    #     return pipe_destination_driver

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
        self.fileinterface.write_content(config_path, rendered_config, open_mode='w')

    def set_raw_config(self, raw_config):
        self.raw_config = raw_config
