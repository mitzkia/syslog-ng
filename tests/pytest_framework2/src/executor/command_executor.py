from subprocess import PIPE
import psutil


class CommandExecutor(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("CommandExecutor")

    def execute_command(self, command):
        self.logger.info("Following command will be executed: [{}]".format(command))
        with psutil.Popen(command, stderr=PIPE, stdout=PIPE) as proc:
            exit_code = proc.wait(timeout=10)
            stdout = str(proc.stdout.read(), 'utf-8')
            stderr = str(proc.stderr.read(), 'utf-8')
        if exit_code != 0:
            self.logger.error("Exit code: [{}]".format(exit_code))
            self.logger.error("Stderr: [{}]".format(stderr))
            self.logger.error("Stdout: [{}]".format(stdout))
        else:
            self.logger.info("Exit code: [{}]".format(exit_code))
        return exit_code, stdout, stderr
