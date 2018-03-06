import os
from src.executors.command.executor import CommandExecutor


class CtlCommandExecutor(object):
    def __init__(self, logger_factory, instance_parameters):
        self.logger_factory = logger_factory
        working_dir = instance_parameters['dir_paths']['working_dir']
        self.syslog_ng_control_tool_path = instance_parameters['binary_file_paths']['syslog_ng_ctl']
        self.syslog_ng_control_socket_path = instance_parameters['file_paths']['control_socket_path']
        self.ctl_commands = {
            "stats": {
                "cmd": ["stats"],
                "stdout": os.path.join(working_dir, "ctl_stats_stdout"),
                "stderr": os.path.join(working_dir, "ctl_stats_stderr")
            },
            "stats_reset": {
                "cmd": ["stats", "--reset"],
                "stdout": os.path.join(working_dir, "ctl_stats_reset_stdout"),
                "stderr": os.path.join(working_dir, "ctl_stats_reset_stderr")
            },
            "query_get": {
                "cmd": ["query", "get"],
                "stdout": os.path.join(working_dir, "ctl_query_get_stdout"),
                "stderr": os.path.join(working_dir, "ctl_query_get_stderr")
            },
            "query_get_sum":  {
                "cmd": ["query", "get", "--sum"],
                "stdout": os.path.join(working_dir, "ctl_query_get_sum_stdout"),
                "stderr": os.path.join(working_dir, "ctl_query_get_sum_stderr")
            },
            "query_reset": {
                "cmd": ["query", "get", "--reset"],
                "stdout": os.path.join(working_dir, "ctl_query_reset_stdout"),
                "stderr": os.path.join(working_dir, "ctl_query_reset_stderr")
            },
            "query_list":  {
                "cmd": ["query", "list"],
                "stdout": os.path.join(working_dir, "ctl_query_list_stdout"),
                "stderr": os.path.join(working_dir, "ctl_query_list_stderr")
            },
            "stop": {
                "cmd": ["stop"],
                "stdout": os.path.join(working_dir, "ctl_stop_stdout"),
                "stderr": os.path.join(working_dir, "ctl_stop_stderr")
            },
            "reload": {
                "cmd": ["reload"],
                "stdout": os.path.join(working_dir, "ctl_reload_stdout"),
                "stderr": os.path.join(working_dir, "ctl_reload_stderr")
            },
            "reopen": {
                "cmd": ["reopen"],
                "stdout": os.path.join(working_dir, "ctl_reopen_stdout"),
                "stderr": os.path.join(working_dir, "ctl_reopen_stderr")
            },
        }

    def slng_ctl_executor(self, cmd_name, query_pattern=None):
        concatenated_command = [self.syslog_ng_control_tool_path]

        for ctl_command_arg in self.ctl_commands[cmd_name]['cmd']:
            concatenated_command.append(ctl_command_arg)

        if query_pattern:
            concatenated_command.append(query_pattern)

        concatenated_command.append("--control={}".format(self.syslog_ng_control_socket_path))
        return CommandExecutor(
            self.logger_factory,
            concatenated_command,
            stdout=self.ctl_commands[cmd_name]['stdout'],
            stderr=self.ctl_commands[cmd_name]['stderr']
        )
