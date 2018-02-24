import os
import signal
import psutil

from src.executor.process_common import ProcessCommon


class ProcessExecutor(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("ProcessExecutor")
        self.process_common = ProcessCommon(logger_factory=logger_factory)

    def start_process(self, command, stdout, stderr):
        self.logger.info("Following process will be started: [{}]".format(command))
        self.logger.debug("LD_LIBRARY_PATH: {}".format(os.environ.get("LD_LIBRARY_PATH")))
        self.logger.debug("JAVA_HOME: {}".format(os.environ.get("JAVA_HOME")))

        process = psutil.Popen(command, stderr=stderr, stdout=stdout)

        self.logger.info("Process started with pid [{}]".format(process.pid))
        return process

    def reload_process(self, process):
        if not self.process_common.is_process_running(process=process):
            raise Exception("process is not running: [{}]".format(process))
        try:
            process.send_signal(signal.SIGHUP)
            self.logger.info("Process [{}] reloaded gracefully".format(process.pid))
        except psutil.TimeoutExpired:
            process.send_signal(signal.SIGSEGV)
            raise Exception("Process can not reloaded gracefully")

    def stop_process(self, process):
        if not self.process_common.is_process_running(process=process):
            raise Exception("process is not running: [{}]".format(process))
        try:
            for child_process in process.children(recursive=True):
                child_process.send_signal(signal.SIGTERM)
            process.send_signal(signal.SIGTERM)
            exit_code = process.wait(timeout=2)
            self.logger.info("Process [{}] stopped gracefully with exit code [{}]".format(process.pid, exit_code))
            return exit_code
        except psutil.TimeoutExpired:
            process.send_signal(signal.SIGSEGV)
            raise Exception("Process can not stopped gracefully")

    @staticmethod
    def kill_process(process):
        process.send_signal(signal.SIGKILL)
        exit_code = process.wait(timeout=2)
        return exit_code
