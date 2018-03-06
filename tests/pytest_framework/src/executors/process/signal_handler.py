import signal
import psutil
from src.executors.process.common import ProcessCommon


class ProcessSignalHandler(ProcessCommon):
    def __init__(self, logger_factory):
        ProcessCommon.__init__(self, logger_factory)
        self.logger = logger_factory.create_logger("ProcessSignalHandler")
        self.exit_code = None

    def reload(self):
        if not self.is_process_running():
            raise Exception("process is not running: [{}]".format(self.process_object))
        try:
            for child_process in self.process_object.children(recursive=True):
                child_process.send_signal(signal.SIGHUP)
            self.process_object.send_signal(signal.SIGHUP)
            self.logger.info("SIGHUP signal sent to process [{}]".format(self.pid))
        except psutil.TimeoutExpired:
            self.process_object.send_signal(signal.SIGSEGV)
            raise Exception("Process can not reloaded gracefully")

    def stop(self):
        if not self.is_process_running():
            raise Exception("process is not running: [{}]".format(self.process_object))
        try:
            for child_process in self.process_object.children(recursive=True):
                child_process.send_signal(signal.SIGTERM)
            self.process_object.send_signal(signal.SIGTERM)
            self.exit_code = self.process_object.wait(timeout=2)
            if self.exit_code != 0:
                self.logger.error("Process [{}] stopped with crash with exit code [{}]".format(self.pid, self.exit_code))
            else:
                self.logger.info(
                    "Process [{}] stopped gracefully with exit code [{}]".format(self.pid, self.exit_code))
            return self.exit_code
        except psutil.TimeoutExpired:
            self.process_object.send_signal(signal.SIGSEGV)
            raise Exception("Process can not stopped gracefully")

    def kill(self):
        self.process_object.send_signal(signal.SIGKILL)
        exit_code = self.process_object.process.wait(timeout=2)
        return exit_code
