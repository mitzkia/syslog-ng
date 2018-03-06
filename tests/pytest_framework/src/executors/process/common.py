import psutil
from src.common.blocking import wait_until_true


class ProcessCommon(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("ProcessCommon")
        self.process_object = None
        self.pid = None

    def is_process_running(self):
        if self.process_object:
            return self.process_object.is_running()

    def is_pid_in_process_list(self):
        return psutil.pid_exists(self.pid)

    def wait_for_pid(self):
        return wait_until_true(self.is_pid_in_process_list)

    def get_opened_file_list(self):
        open_files = self.process_object.open_files()
        if open_files:
            self.logger.error("Found remaining open files: %s" % open_files)
        return open_files

    def dump_process_information(self):
        self.logger.info("Process information: [{}]".format(str(self.process_object.as_dict())))
