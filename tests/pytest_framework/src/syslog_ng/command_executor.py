import os
from src.executors.command.executor import CommandExecutor
from src.driver_io.file_based.file import File


class SlngCommandExecutor(object):
    def __init__(self, logger_factory, instance_parameters):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SlngCommandExecutor")
        syslog_ng_binary_path = instance_parameters['binary_file_paths']['syslog_ng_binary']
        self.working_dir = instance_parameters['dir_paths']['working_dir']
        config_path = instance_parameters['file_paths']['config_path']
        self.slng_commands = {
            "get_version": {
                "cmd": [syslog_ng_binary_path, "--version"],
                "stdout": os.path.join(self.working_dir, "slng_version_stdout"),
                "stderr": os.path.join(self.working_dir, "slng_version_stderr")
            },
            "syntax_only": {
                "cmd": [syslog_ng_binary_path, "--enable-core", "--syntax-only", "--cfgfile={}".format(config_path)],
                "stdout": os.path.join(self.working_dir, "slng_syntax_only_stdout"),
                "stderr": os.path.join(self.working_dir, "slng_syntax_only_stderr"),
            },
            "gdb_bt_full": {
                "cmd": ["gdb", "-ex", "bt full", "--batch", syslog_ng_binary_path, "--core"],
                "stdout": os.path.join(self.working_dir, "core_stdout.backtrace"),
                "stderr": os.path.join(self.working_dir, "core_stderr.backtrace")
            }
        }
        self.core_detected = False

    def slng_executor(self, cmd_name, core_file=None):
        if core_file:
            self.slng_commands[cmd_name]['cmd'].append(core_file)
        return CommandExecutor(
            self.logger_factory,
            self.slng_commands[cmd_name]['cmd'],
            stdout=self.slng_commands[cmd_name]['stdout'],
            stderr=self.slng_commands[cmd_name]['stderr']
        )

    def is_core_file_exist(self):
        found_core_files = File(self.logger_factory, "core*").get_files_by_pattern()
        if found_core_files:
            for core_file in found_core_files:
                self.core_detected = True
                self.slng_executor("gdb_bt_full", core_file=core_file)
                File(self.logger_factory, core_file).move_file("{}/".format(self.working_dir))
                raise Exception("syslog-ng core file found and processed")
