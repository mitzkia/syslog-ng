import psutil
from mockito import when, args, unstub
from src.parameters.testcase_parameters import TestCaseParameters
from src.parameters.syslog_ng_parameters import SyslogNgParameters
from src.logger.logger_factory import LoggerFactory
from src.registers.file_register import FileRegister
from src.driver_io.file_based.file import File
from src.executor.process_common import ProcessCommon

class SetupUnitTestCase(object):
    def __init__(self, testcase_context):
        testcase_context = testcase_context
        testcase_parameters = TestCaseParameters(testcase_context)
        self.syslog_ng_parameters = SyslogNgParameters(testcase_context, testcase_parameters)

        when(self.syslog_ng_parameters.testcase_context).getfixturevalue("installdir").thenReturn("/tmp/fake_install_dir")
        fake_fd = open("/tmp/fake_stdout_stderr_path", 'w')
        when(self.syslog_ng_parameters).open_file_for_write(*args).thenReturn(fake_fd)
        fake_fd.close()

        self.logger_factory = LoggerFactory(
            report_file_path="",
            loglevel="info",
            use_console_handler=True,
            use_file_handler=False
        )
        self.logger = self.logger_factory.create_logger("UnitTest")

        self.file_register = FileRegister(self.logger_factory, "/tmp")
        testcase_context.addfinalizer(self.teardown)

    def teardown(self):
        for _registered_file_path_key, registered_file_path in self.file_register.registered_files.items():
            file_object = File(self.logger_factory, registered_file_path)
            if file_object.is_file_exist():
                file_object.delete_file()
        unstub()
        ProcessCommon(self.logger_factory).get_opened_file_list(psutil.Process())
