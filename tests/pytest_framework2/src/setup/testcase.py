import os
import py
from src.parameters.testcase_parameters import TestCaseParameters
from src.parameters.syslog_ng_parameters import SyslogNgParameters
from src.logger.logger_factory import LoggerFactory
from src.registers.file_register import FileRegister
from src.message.message_interface import MessageInterface


class SetupTestCase(object):
    def __init__(self, testcase_context):
        testcase_parameters = TestCaseParameters(testcase_context)
        self.syslog_ng_parameters = SyslogNgParameters(testcase_context, testcase_parameters)
        self.prepare_testcase_working_dir(testcase_parameters)

        self.logger_factory = LoggerFactory(
            report_file_path=testcase_parameters['file_paths']['report_file'],
            loglevel=testcase_parameters['loglevel'],
            use_console_handler=False,
            use_file_handler=True
        )
        self.logger = self.logger_factory.create_logger("SetupTestCase")

        self.file_register = None
        self.message = None
        self.instantiate_main_interfaces(testcase_parameters)

        self.teardown_actions = []
        testcase_context.addfinalizer(self.teardown, testcase_context)

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

    def teardown(self, testcase_context):
        for inner_function in self.teardown_actions:
            try:
                inner_function()
            except OSError:
                pass
        self.log_assertion_error(testcase_context)

    def log_assertion_error(self, testcase_context):
        terminalreporter = testcase_context.config.pluginmanager.getplugin('terminalreporter')
        if terminalreporter.stats.get('failed'):
            for failed_report in terminalreporter.stats.get('failed'):
                if failed_report.location[2] == testcase_context.node.name:
                    self.logger.error(str(failed_report.longrepr))

    # Helper functions for functional tests
    def new_bsd_message(self, message_parts=None, message_counter=1):
        return self.message.construct_bsd_messages(message_parts, message_counter)

    def new_syslog_message(self, message_parts=None, message_counter=1):
        return self.message.construct_ietf_messages(message_parts, message_counter)

    def new_file_path(self, prefix, extension="log"):
        return self.file_register.get_registered_file_path(prefix=prefix, extension=extension)
