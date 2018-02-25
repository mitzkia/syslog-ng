import os
from src.executors.process.interface import ProcessInterface


class SlngProcessExecutor(object):
    def __init__(self, logger_factory, instance_parameters):
        self.logger_factory = logger_factory
        self.process_interface = ProcessInterface(logger_factory)
        working_dir = instance_parameters['dir_paths']['working_dir']
        syslog_ng_binary_path = instance_parameters['binary_file_paths']['syslog_ng_binary']
        config_path = instance_parameters['file_paths']['config_path']
        persist_path = instance_parameters['file_paths']['persist_path']
        pid_path = instance_parameters['file_paths']['pid_path']
        control_socket_path = instance_parameters['file_paths']['control_socket_path']
        self.process_commands = {
            "start": {
                "cmd": [syslog_ng_binary_path, "-Fedtv", "--no-caps", "--enable-core", "-f", config_path, "-R", persist_path, "-p", pid_path, "-c", control_socket_path],
                "stdout": os.path.join(working_dir, "slng_process_stdout"),
                "stderr": os.path.join(working_dir, "slng_process_stderr"),
            },
            "strace": {
                "cmd": ["strace", "-s", "8888", "-ff", "-o", os.path.join(working_dir, 'strace.log')],
                "stdout": os.path.join(working_dir, "slng_strace_stdout"),
                "stderr": os.path.join(working_dir, "slng_strace_stderr"),
            },
            "perf": {
                "cmd": ["perf", "record", "-g", "-v", "-s", "-F", "99", "--output={}".format(os.path.join(working_dir, 'perf.log'))],
                "stdout": os.path.join(working_dir, "slng_perf_stdout"),
                "stderr": os.path.join(working_dir, "slng_perf_stderr"),
            },
            "valgrind": {
                "cmd": [
                    "valgrind",
                    "--run-libc-freeres=no",
                    "--show-leak-kinds=all",
                    "--track-origins=yes",
                    "--tool=memcheck",
                    "--leak-check=full",
                    "--keep-stacktraces=alloc-and-free",
                    "--read-var-info=yes",
                    "--error-limit=no",
                    "--num-callers=40",
                    "--verbose",
                    "--log-file={}".format(os.path.join(working_dir, 'valgrind.log'))
                ],
                "stdout": os.path.join(working_dir, "slng_valgrind_stdout"),
                "stderr": os.path.join(working_dir, "slng_valgrind_stderr"),
            },
        }

    def slng_process_start(self):
        return self.process_interface.start(
            self.process_commands['start']['cmd'],
            self.process_commands['start']['stdout'],
            self.process_commands['start']['stderr'])

    def slng_process_start_behind(self, parent_cmd_name):
        concatenated_command = self.process_commands[parent_cmd_name]['cmd'] + self.process_commands['start']['cmd']
        return self.process_interface.start(
            concatenated_command,
            self.process_commands[parent_cmd_name]['stdout'],
            self.process_commands[parent_cmd_name]['stderr'])

    def slng_process_reload(self):
        return self.process_interface.reload()

    def slng_process_stop(self):
        return self.process_interface.stop()

    def get_process(self):
        return self.process_interface.process_object

    def get_pid(self):
        return self.process_interface.pid

    def slng_is_running(self):
        return self.process_interface.is_process_running()
