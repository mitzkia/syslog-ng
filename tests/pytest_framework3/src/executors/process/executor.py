import psutil
from src.executors.process.common import ProcessCommon


class ProcessExecutor(ProcessCommon):
    def __init__(self, logger_factory):
        ProcessCommon.__init__(self, logger_factory)
        self.logger = logger_factory.create_logger("ProcessExecutor")
        self.process_object = None
        self.pid = None

    def start(self, command_of_process, stdout, stderr):
        self.logger.info("Following process will be started: [{}]".format(" ".join(command_of_process)))
        stdout_fd = open(stdout, 'a')
        stderr_fd = open(stderr, 'a')
        self.process_object = psutil.Popen(command_of_process, stderr=stderr_fd, stdout=stdout_fd)
        self.pid = self.process_object.pid
        self.logger.info("Process started with pid [%s]" % self.pid)
        return self.process_object
