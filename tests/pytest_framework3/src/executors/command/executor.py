import psutil


class CommandExecutor(object):
    def __init__(self, logger_factory, command, stdout, stderr):
        self.logger = logger_factory.create_logger("CommandExecutor")
        self.command = command
        self.exit_code = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdout_content = None
        self.stderr_content = None
        self.execute_command()
        self.evaluate_exit_code()

    def execute_command(self):
        self.logger.debug("Following command will be executed: {}".format(" ".join(self.command)))
        stdout_fd = open(self.stdout, 'a')
        stderr_fd = open(self.stderr, 'a')
        with psutil.Popen(self.command, stderr=stderr_fd, stdout=stdout_fd) as proc:
            self.exit_code = proc.wait(timeout=10)

    def get_stdout(self):
        return self.stdout_content

    def get_stderr(self):
        return self.stderr_content

    def get_exit_code(self):
        return self.exit_code

    def get_all(self):
        return self.exit_code, self.stdout_content, self.stderr_content

    def get_command(self):
        return self.command

    def evaluate_exit_code(self):
        with open(self.stdout, 'r') as file_object:
            self.stdout_content = file_object.read()
        with open(self.stderr, 'r') as file_object:
            self.stderr_content = file_object.read()

        if (self.exit_code != 0) and (self.exit_code != -15) and (self.exit_code != 1):
            self.logger.error("Exit code: [{}]".format(self.exit_code))
            self.logger.error("All Stderr for this command: [{}]".format(self.stderr_content))
            self.logger.error("All Stdout for this command: [{}]".format(self.stdout_content))
        else:
            self.logger.debug("Exit code: [{}]".format(self.exit_code))
            self.logger.debug("All Stderr for this command: [{}]".format(self.stderr_content))
            self.logger.debug("All Stdout for this command: [{}]".format(self.stdout_content))
