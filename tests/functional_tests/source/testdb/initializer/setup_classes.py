from source.testdb.common.common import get_current_date, get_testcase_name
from source.testdb.path.path_database import TestdbPathDatabase
from source.testdb.config.config_context import TestdbConfigContext
from source.testdb.logger.logger import TestdbLogger
from source.register.file import FileRegister


class SetupClasses(object):
    def __init__(self, testcase_context, topology="server"):
        self.testcase_context = testcase_context
        self.topology = topology

        self.current_date = get_current_date()
        self.testcase_name = get_testcase_name(self.testcase_context)
        self.log_writer = None

        self.instantiate_classes()
        self.testcase_context.addfinalizer(self.teardown)

    def instantiate_classes(self):
        if self.topology == "server":
            self.init_classes_for_topology(testcase_context=self.testcase_context, topology="server")
        elif self.topology == "client_server":
            self.init_classes_for_topology(testcase_context=self.testcase_context, topology="server")
            self.init_classes_for_topology(testcase_context=self.testcase_context, topology="client")
        else:
            print("Unknown defined topology: [%s]" % self.topology)
            assert False

    def init_classes_for_topology(self, testcase_context, topology):
        setattr(self, "testdb_path_database_for_%s" % topology,
                TestdbPathDatabase(
                    testcase_name=self.testcase_name,
                    topology=topology,
                    current_date=self.current_date
                ))
        setattr(self, "testdb_config_context_for_%s" % topology,
                TestdbConfigContext(
                    testdb_path_database=getattr(self, "testdb_path_database_for_%s" % topology),
                    testcase_context=testcase_context
                ))
        setattr(self, "testdb_logger_for_%s" % topology,
                TestdbLogger(
                    testdb_path_database=getattr(self, "testdb_path_database_for_%s" % topology),
                    testdb_config_context=getattr(self, "testdb_config_context_for_%s" % topology)
                ))

        self.log_writer = self.testdb_logger_for_server.set_logger(logsource="SetupClasses")
        self.log_writer.info("=============================Testcase start: [%s]================================" % self.testcase_name)
        self.log_writer.info(">>> Testcase log file: %s", getattr(self, "testdb_path_database_for_%s" % topology).testcase_report_file)
        self.log_writer.info(">>> Testcase log level: %s", getattr(self, "testdb_config_context_for_%s" % topology).log_level)

        setattr(self, "file_register_for_%s" % topology,
                FileRegister(
                    testdb_logger=getattr(self, "testdb_logger_for_%s" % topology),
                    testdb_path_database=getattr(self, "testdb_path_database_for_%s" % topology),
                ))

        if topology == "server":
            self.testdb_path_database = self.testdb_path_database_for_server
            self.testdb_config_context = self.testdb_config_context_for_server
            self.testdb_logger = self.testdb_logger_for_server

            self.file_register = self.file_register_for_server

    def teardown(self):
        self.log_writer.info("=============================Testcase finish: [%s]================================" % self.testcase_name)
        self.log_writer.info(">>> Testcase log file: %s" % self.testdb_path_database.testcase_report_file)

