import os
import py

from src.runtimeparameters.runtimeparameters import RuntimeParameters
from src.logger.logger_factory import LoggerFactory
from src.fileregister.file import FileRegister
from src.message.message_interface import MessageInterface
from src.syslogng.syslogng import SyslogNg
from src.syslogngconfig.syslogngconfig import SyslogNgConfig
from src.syslogngpath.syslogngpath import SyslogNgPath


class SetupTestCase(object):
    def __init__(self, testcase_context):
        self.testcase_context = testcase_context
        self.runtime_parameters = RuntimeParameters(self.testcase_context)
        self.prepare_testcase_working_dir(self.runtime_parameters)

        self.logger_factory = LoggerFactory(self.runtime_parameters['report_file'],
                                            self.runtime_parameters['loglevel'],
                                            use_console_handler=False)
        self.logger = self.logger_factory.create_logger("SetupTestCase")

        self.instantiate_main_interfaces()

        self.teardown_actions = []
        testcase_context.addfinalizer(self.teardown)

    def prepare_testcase_working_dir(self, runtime_parameters):
        working_directory = runtime_parameters["working_dir"]
        if not os.path.exists(working_directory):
            os.makedirs(working_directory)
        testcase_path = runtime_parameters["testcase_path"]
        testcase_path.copy(py.path.local(self.runtime_parameters['working_dir']))

    def instantiate_main_interfaces(self):
        self.file_register = FileRegister(self.logger_factory, self.runtime_parameters['working_dir'])
        self.message = MessageInterface(self.logger_factory)
        self.syslogngpath = SyslogNgPath(self.runtime_parameters)

    def log_assertion_error(self):
        terminalreporter = self.testcase_context.config.pluginmanager.getplugin('terminalreporter')
        if terminalreporter.stats.get('failed'):
            for failed_report in terminalreporter.stats.get('failed'):
                if failed_report.location[2] == self.testcase_context.node.name:
                    self.logger.error(str(failed_report.longrepr))

    def teardown(self):
        for inner_function in self.teardown_actions:
            try:
                inner_function()
            except:
                pass
        self.log_assertion_error()

    # Helper functions for test cases
    def new_bsd_message(self, message_parts=None, message_counter=1):
        if message_counter == 1:
            return self.message.create_bsd_message(defined_bsd_message_parts=message_parts)
        return self.message.create_multiple_bsd_messages(defined_bsd_message_parts=message_parts, message_counter=message_counter)

    def new_syslog_message(self, message_parts=None, message_counter=1):
        if message_counter == 1:
            return self.message.create_ietf_message(defined_ietf_message_parts=message_parts)
        return self.message.create_multiple_ietf_messages(defined_ietf_message_parts=message_parts, message_counter=message_counter)

    def new_file_path(self, prefix, extension="log"):
        return self.file_register.get_registered_file_path(prefix=prefix, extension=extension)

    def new_config(self, instance_name="server"):
        return SyslogNgConfig(self.syslogngpath, self.logger_factory, self.file_register, instance_name)

    def new_syslog_ng(self, instance_name="server"):
        syslog_ng = SyslogNg(self.syslogngpath, self.logger_factory, instance_name)
        self.teardown_actions.append(syslog_ng.stop)
        return syslog_ng


class SetupUnitTestCase(object):
    def __init__(self, testcase_context):
        self.runtime_parameters = {
            "working_dir": "",
            "working_dir_relative": "",
            "report_file": "",
            "testcase_name": testcase_context.node.name,
            "testcase_path": testcase_context.node.fspath,
            "install_dir": "",
            "syslog_ng_version": "3.13",
            "libjvm_dir": "/usr/lib/jvm/default-java/jre/lib/amd64/server/",
            "loglevel": "info"
        }
        self.logger_factory = LoggerFactory(
            self.runtime_parameters['report_file'], 
            self.runtime_parameters['loglevel'], 
            use_file_handler=False)
