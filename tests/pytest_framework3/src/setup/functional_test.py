import os
import py
from src.parameters.test_case import TestCaseParameters
from src.parameters.syslog_ng import SyslogNgParameters
from src.logger.logger_factory import LoggerFactory
from src.registers.file import FileRegister
from src.message.interface import MessageInterface
from src.syslog_ng_config.interface import ConfigInterface
from src.syslog_ng.syslog_ng import SyslogNg


class SetupTestCase(object):
    def __init__(self, testcase_context):
        self.testcase_context = testcase_context
        self.testcase_parameters = TestCaseParameters(testcase_context)
        self.syslog_ng_parameters = SyslogNgParameters(testcase_context, self.testcase_parameters)
        self.prepare_testcase_working_dir(self.testcase_parameters)

        self.logger_factory = LoggerFactory(
            report_file_path=self.testcase_parameters['file_paths']['report_file'],
            loglevel=self.testcase_parameters['loglevel']
        )
        self.logger = self.logger_factory.create_logger("Setup", use_console_handler=True, use_file_handler=True)
        self.logger.info(">>> Testcase setup start:{}".format(self.testcase_parameters['testcase_name']))

        self.file_register = None
        self.message = None
        self.instantiate_main_interfaces(self.testcase_parameters)
        self.logger.info(">>> Testcase setup finish:{}".format(self.testcase_parameters['testcase_name']))
        self.teardown_actions = []
        testcase_context.addfinalizer(self.teardown)

    @staticmethod
    def prepare_testcase_working_dir(testcase_parameters):
        working_directory = testcase_parameters['dir_paths']["working_dir"]
        if not os.path.exists(working_directory):
            os.makedirs(working_directory)
        testcase_file = testcase_parameters['file_paths']["testcase_file"]
        testcase_file.copy(py.path.local(testcase_parameters['dir_paths']['working_dir']))

    def instantiate_main_interfaces(self, testcase_parameters):
        self.file_register = FileRegister(self.logger_factory, testcase_parameters['dir_paths']['working_dir'])
        self.message = MessageInterface(self.logger_factory)

    def teardown(self):
        self.logger.info(">>> Testcase teardown start:{}".format(self.testcase_parameters['testcase_name']))
        for inner_function in self.teardown_actions:
            try:
                inner_function()
            except OSError:
                pass
        self.log_assertion_error()
        self.logger = self.logger_factory.create_logger("Teardown", use_console_handler=True, use_file_handler=True)
        self.logger.info(">>> Testcase teardown finish:{}".format(self.testcase_parameters['testcase_name']))

    def log_assertion_error(self):
        terminalreporter = self.testcase_context.config.pluginmanager.getplugin('terminalreporter')
        if terminalreporter.stats.get('failed'):
            for failed_report in terminalreporter.stats.get('failed'):
                if failed_report.location[2] == self.testcase_context.node.name:
                    self.logger = self.logger_factory.create_logger("Teardown", use_console_handler=False, use_file_handler=True)
                    self.logger.error(str(failed_report.longrepr))

    # Helper functions for functional tests
    def new_bsd_message(self, message_parts=None, message_counter=1):
        return self.message.construct_bsd_messages(message_parts, message_counter)

    def new_syslog_message(self, message_parts=None, message_counter=1):
        return self.message.construct_ietf_messages(message_parts, message_counter)

    def new_file_path(self, prefix, extension="log"):
        return self.file_register.get_registered_file_path(prefix=prefix, extension=extension)

    def new_config(self, instance_name="server"):
        return ConfigInterface(self.logger_factory, self.syslog_ng_parameters, self.file_register, instance_name)

    def new_syslog_ng(self, instance_name="server"):
        syslog_ng = SyslogNg(self.logger_factory, self.syslog_ng_parameters, instance_name)
        self.teardown_actions.append(syslog_ng.stop)
        return syslog_ng
