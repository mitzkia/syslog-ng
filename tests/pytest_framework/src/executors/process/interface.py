from src.executors.process.executor import ProcessExecutor
from src.executors.process.signal_handler import ProcessSignalHandler


class ProcessInterface(ProcessExecutor, ProcessSignalHandler):
    def __init__(self, logger_factory):
        ProcessExecutor.__init__(self, logger_factory)
        ProcessSignalHandler.__init__(self, logger_factory)
        self.process_object = None
        self.pid = None
        self.exit_code = None

    def get_process(self):
        return self.process_object

    def get_pid(self):
        return self.pid

    def get_exit_code(self):
        return self.exit_code
