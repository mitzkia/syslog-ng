import os
import shlex
from subprocess import PIPE
import psutil


class RuntimeParameters(dict):
    def __init__(self, testcase_context):
        testcase_name = self.get_testcase_name(testcase_context)
        reports_path = testcase_context.getfixturevalue("reports")
        relative_path = os.path.join(reports_path, testcase_name)
        testcase_working_dir = self.get_testcase_working_dir(self.framework_root_dir(), relative_path)
        testcase_report_file = self.get_testcase_report_file(testcase_working_dir, testcase_name)
        syslog_ng_version = self.get_syslog_ng_version(testcase_context.getfixturevalue("installpath"))

        runtime_parameters = {
            "working_dir": testcase_working_dir,
            "working_dir_relative": relative_path,
            "report_file": testcase_report_file,
            "testcase_name": testcase_name,
            "testcase_path": testcase_context.node.fspath,
            "install_dir": testcase_context.getfixturevalue("installpath"),
            "syslog_ng_version": syslog_ng_version,
            "libjvm_dir": "/usr/lib/jvm/default-java/jre/lib/amd64/server/",
            "loglevel": testcase_context.getfixturevalue("loglevel")
        }
        os.environ["LD_LIBRARY_PATH"] = runtime_parameters['libjvm_dir']
        super().__init__(runtime_parameters)

    @staticmethod
    def get_testcase_name(testcase_context):
        if not testcase_context.node.name:
            raise Exception("Can not parse testcase name")
        return testcase_context.node.name

    @staticmethod
    def framework_root_dir():
        return os.getcwd()

    @staticmethod
    def get_testcase_working_dir(root_dir, relative_path):
        return os.path.join(root_dir, relative_path)

    @staticmethod
    def get_testcase_report_file(testcase_working_dir, testcase_name):
        return os.path.join(testcase_working_dir, "testcase_%s.log" % testcase_name)

    @staticmethod
    def get_syslog_ng_version(syslog_ng_installpath):
        syslog_ng_binary_path = os.path.join(syslog_ng_installpath, 'sbin/syslog-ng')
        if not os.path.exists(syslog_ng_binary_path):
            raise Exception("syslog-ng binary driver_file did not exist, given installpath could be wrong: [%s]" % syslog_ng_installpath)
        command = "%s --version" % syslog_ng_binary_path
        command_args = shlex.split(command)
        with psutil.Popen(command_args, stderr=PIPE, stdout=PIPE) as proc:
            syslog_ng_version_output = str(proc.stdout.read(), 'utf-8')

        for syslog_ng_version_output_line in syslog_ng_version_output.splitlines():
            if "Config version:" in syslog_ng_version_output_line:
                return syslog_ng_version_output_line.split()[2]
        raise Exception("Can not parse 'Config version' from ./syslog-ng --version")
