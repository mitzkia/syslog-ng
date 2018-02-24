import os
import signal
import psutil

from src.executor.process_common import ProcessCommon


class ProcessExecutor(object):
    def __init__(self, logger_factory, working_dir):
        self.logger = logger_factory.create_logger("ProcessExecutor")
        self.testcase_working_dir = working_dir
        self.process_common = ProcessCommon(logger_factory=logger_factory)
        self.external_commands = {
            "strace": ["strace", "-s", "8888", "-ff", "-o", os.path.join(self.testcase_working_dir, 'strace.log')],
            "valgrind": ["valgrind", "--show-leak-kinds=all", "--track-origins=yes", "--tool=memcheck", "--leak-check=full", "--log-driver_file=%s" % (os.path.join(self.testcase_working_dir, 'valgrind.log'))],
            "perf": ["perf", "record", "-g", "-v", "-s", "-F", "99", "--output=%s" % (os.path.join(self.testcase_working_dir, 'perf.log'))]
        }

    def start_process(self, command, stdout, stderr, external_tool=None):
        if external_tool:
            command = self.set_external_tool_for_command(command=command, external_tool=external_tool)
        self.logger.info("Following process will be started: [%s]" % command)
        self.logger.debug("LD_LIBRARY_PATH: %s" % os.environ.get("LD_LIBRARY_PATH"))
        self.logger.debug("JAVA_HOME: %s" % os.environ.get("JAVA_HOME"))

        process = psutil.Popen(command, stderr=stderr, stdout=stdout)

        self.logger.info("Process started with pid [%s]" % process.pid)
        return process

    def reload_process(self, process):
        if not self.process_common.is_process_running(process=process):
            raise Exception("process is not running: [%s]" % process)
        try:
            process.send_signal(signal.SIGHUP)
            self.logger.info("Process [%s] reloaded gracefully" % process.pid)
        except psutil.TimeoutExpired:
            process.send_signal(signal.SIGSEGV)
            raise Exception("Process can not reloaded gracefully")

    def stop_process(self, process):
        if not self.process_common.is_process_running(process=process):
            raise Exception("process is not running: [%s]" % process)
        try:
            for child_process in process.children(recursive=True):
                child_process.send_signal(signal.SIGTERM)
            process.send_signal(signal.SIGTERM)
            exit_code = process.wait(timeout=2)
            self.logger.info("Process [%s] stopped gracefully with exit code [%s]" % (process.pid, exit_code))
            return exit_code
        except psutil.TimeoutExpired:
            process.send_signal(signal.SIGSEGV)
            raise Exception("Process can not stopped gracefully")

    @staticmethod
    def kill_process(process):
        process.send_signal(signal.SIGKILL)
        exit_code = process.wait(timeout=2)
        return exit_code

    def set_external_tool_for_command(self, command, external_tool):
        return self.external_commands[external_tool].append(command)
