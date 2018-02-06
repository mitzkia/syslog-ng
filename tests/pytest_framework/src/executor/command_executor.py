import shlex
import psutil
from subprocess import PIPE


class CommandExecutor(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("CommandExecutor")

    def execute_command(self, command):
        command_args = shlex.split(command)
        self.logger.info("Following command will be executed: [%s]" % command)
        with psutil.Popen(command_args, stderr=PIPE, stdout=PIPE) as proc:
            exit_code = proc.wait(timeout=10)
            stdout = str(proc.stdout.read(), 'utf-8')
            stderr = str(proc.stderr.read(), 'utf-8')
        if exit_code != 0:
            self.logger.error("Exit code: [%s]" % exit_code)
            self.logger.error("Stderr: [%s]" % stderr)
            self.logger.error("Stdout: [%s]" % stdout)
        else:
            self.logger.info("Exit code: [%s]" % exit_code)
        return exit_code, stdout, stderr
