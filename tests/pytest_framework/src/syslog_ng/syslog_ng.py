from src.syslog_ng.command_executor import SlngCommandExecutor
from src.syslog_ng.process_executor import SlngProcessExecutor
from src.syslog_ng.console_handler import SlngConsoleHandler
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl


class SyslogNg(SlngCommandExecutor, SlngProcessExecutor, SlngConsoleHandler):
    def __init__(self, logger_factory, syslog_ng_parameters, instance_name):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SyslogNg")
        instance_parameters = syslog_ng_parameters.set_instance_parameters(instance_name)
        SlngCommandExecutor.__init__(self, logger_factory, instance_parameters)
        SlngProcessExecutor.__init__(self, logger_factory, instance_parameters)
        SlngConsoleHandler.__init__(self, logger_factory, self.process_commands, self.slng_commands)
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        self.external_tool = None

    def start(self, syslog_ng_config, external_tool=None, expected_run=True):
        self.logger.info(">>> Beginning of syslog-ng start")
        self.external_tool = external_tool
        syslog_ng_config.write_config_content()

        exit_code = self.slng_executor(cmd_name="syntax_only").get_exit_code()
        if not self.evaluate_syntax_only(expected_run, exit_code):
            return None

        if external_tool:
            self.slng_process_start_behind(parent_cmd_name=external_tool)
        else:
            self.slng_process_start()
        self.evaluate_process_start()
        self.logger.info(">>> End of syslog-ng start")

    def reload(self, syslog_ng_config):
        self.logger.info(">>> Beginning of syslog-ng reload")
        syslog_ng_config.write_config_content()
        self.slng_process_reload()
        self.evaluate_process_reload()
        self.logger.info(">>> End of syslog-ng reload")

    def stop(self):
        if not self.core_detected and self.slng_is_running():
            self.logger.info(">>> Beginning of syslog-ng stop")
            if self.slng_process_stop() != 0:
                self.is_core_file_exist()
            self.evaluate_process_stop()
            self.logger.info(">>> End of syslog-ng stop")

    def evaluate_syntax_only(self, expected_run, exit_code):
        if expected_run and (exit_code != 0):
            self.dump_console_log()
            raise Exception("syslog-ng can not start with config")
        elif (not expected_run) and (exit_code != 0):
            self.logger.info("syslog-ng can not started, but this was the expected behaviour")
            return None
        else:
            self.logger.debug("syslog-ng can started with config")
            return True

    def evaluate_process_start(self):
        if not self.wait_for_start_message(external_tool=self.external_tool) or not self.syslog_ng_ctl.wait_for_control_socket_start():
            raise Exception("syslog-ng can not started (a syslog-ng start kriteriumok nem teljesultek), check if core file detected")

    def evaluate_process_reload(self):
        if not self.wait_for_reload_message(external_tool=self.external_tool) or not self.syslog_ng_ctl.wait_for_control_socket_start():
            raise Exception("syslog-ng can not reloaded check if core file detected")

    def evaluate_process_stop(self):
        if not self.wait_for_stop_message(external_tool=self.external_tool) or not self.syslog_ng_ctl.wait_for_control_socket_stop():
            raise Exception("syslog-ng can not stopped, check if core file detected")

    # def dump_config(self):
    #     File(self.logger_factory, self.instance_parameters['file_paths']['config_path']).dump_content()
    #
    # def dump_console_log(self):
    #     return File(self.logger_factory, self.instance_parameters['file_paths']['stderr_path']).dump_content()
