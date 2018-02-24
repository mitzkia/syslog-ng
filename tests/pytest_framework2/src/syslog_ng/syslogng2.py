import os
import psutil


class CmdExecutor(object):
    def __init__(self, command):
        self.command = command
        self.exit_code = None
        self.stdout = None
        self.stderr = None
        self.execute_command(command)

    def execute_command(self, command):
        self.exit_code = "62"

    def get_stdout(self):
        return self.stdout

    def get_stderr(self):
        return self.stderr

    def get_exit_code(self):
        return self.exit_code

    def get_all(self):
        return self.exit_code, self.stdout, self.stderr

    def get_command(self):
        return self.command

class ProcessCommon(object):
    def __init__(self):
        pass

    @staticmethod
    def is_pid_in_process_list(pid):
        return psutil.pid_exists(pid)

class ProcessExecutor(ProcessCommon):
    def __init__(self, command_of_process):
        ProcessCommon.__init__(self)
        self.command_of_process = command_of_process
        self.exit_code = None
        self.pid = None
        self.process_object = None

    def start(self):
        self.process_object = "EEE"
        # Fixme wait_until_true
        self.is_pid_in_process_list(self.pid)

    def reload(self):
        pass

    def stop(self):
        pass

    def is_pid_in_process_list(self):
        pass

    def get_exit_code(self):
        return self.exit_code

    def get_pid(self):
        return self.pid

    def get_process(self):
        return self.process_object

    def get_all(self):
        return self.exit_code, self.pid, self.process_object

    def get_command(self):
        return self.command_of_process

class SlngCtlExecutor(object):
    def __init__(self):
        self.commands = {
            "stats": ["ls", "-la"]
        }

    def slng_ctl_executor(self, cmd_name):
        return CmdExecutor(self.commands[cmd_name])

class SlngCmdExecutor(object):
    def __init__(self, instance_parameters):
        syslog_ng_binary_path = instance_parameters['binary_file_paths']['syslog_ng_binary']
        config_path = instance_parameters['file_paths']['config_path']
        self.commands = {
            "version": [syslog_ng_binary_path, "--version"],
            "syntax_check": [syslog_ng_binary_path, "-Fedtv --no-caps --enable-core --syntax-check", "-f", config_path],
            "gdb_bt_full": ["gdb", "--core", os.path.join(os.getcwd(), "core*"), syslog_ng_binary_path, '-ex', 'bt full', '--batch']
        }

    def slng_executor(self, cmd_name):
        return CmdExecutor(self.commands[cmd_name])

class SlngProcessRunner(object):
    def __init__(self, instance_parameters):
        working_dir = instance_parameters['dir_paths']['working_dir']
        syslog_ng_binary_path = instance_parameters['binary_file_paths']['syslog_ng_binary']
        config_path = instance_parameters['file_paths']['config_path']
        persist_path = instance_parameters['file_paths']['persist_path']
        pid_path = instance_parameters['file_paths']['pid_path']
        control_socket_path = instance_parameters['file_paths']['control_socket_path']
        self.process_commands = {
            "start": [syslog_ng_binary_path, "-Fedtv --no-caps --enable-core", "-f", config_path, "-R", persist_path, "-p", pid_path, "-c", control_socket_path],
            "strace": ["strace", "-s", "8888", "-ff", "-o", os.path.join(working_dir, 'strace.log')],
            "perf": ["perf", "record", "-g", "-v", "-s", "-F", "99", "--output={}".format(os.path.join(working_dir, 'perf.log'))],
            "valgrind": ["valgrind", "--show-leak-kinds=all", "--track-origins=yes", "--tool=memcheck", "--leak-check=full", "--log-driver_file={}".format((os.path.join(working_dir, 'valgrind.log')))],
            "reload": [""],
            "stop": [""],
        }

    def slng_process_runner(self, cmd_name):
        return ProcessExecutor(self.process_commands[cmd_name])

    def slng_start_behind(self, parent_cmd_name):
        return ProcessExecutor(self.process_commands[parent_cmd_name]+self.process_commands['start'])

class SlngConsoleHandler(object):
    def __init__(self, instance_parameters):
        stderr_path = ""
        stderr_fd = ""

    def wait_for_start_message(self):
        pass

class SyslogNgCtl(SlngCtlExecutor):
    def __init__(self):
        SlngCmdExecutor.__init__(self)


class SyslogNg(SlngCmdExecutor, SlngProcessRunner, SlngConsoleHandler):
    def __init__(self):
        working_dir = "/workdir"
        install_dir = "/installdir"
        instance_name = "server"
        relative_working_dir = "/relative_working_dir"
        instance_parameters = {
            "dir_paths": {
                "working_dir": working_dir,
                "install_dir": install_dir,
                "libjvm_dir": "/usr/lib/jvm/default-java/jre/lib/amd64/server/"
            },
            "file_paths": {
                "stdout_path": os.path.join(*[working_dir, 'syslog_ng_stdout_{}.log'.format(instance_name)]),
                "stderr_path": os.path.join(*[working_dir, 'syslog_ng_stderr_{}.log'.format(instance_name)]),
                "config_path": os.path.join(*[working_dir, 'syslog_ng_{}.conf'.format(instance_name)]),
                "persist_path": os.path.join(*[working_dir, 'syslog_ng_{}.persist'.format(instance_name)]),
                "pid_path": os.path.join(*[working_dir, 'syslog_ng_{}.pid'.format(instance_name)]),
                "control_socket_path": os.path.join(*[relative_working_dir, 'syslog_ng_{}.ctl'.format(instance_name)]),
            },
            "binary_file_paths": {
                "syslog_ng_binary": os.path.join(*[install_dir, "sbin/syslog-ng"]),
                "syslog_ng_ctl": os.path.join(*[install_dir, "sbin/syslog-ng-ctl"]),
            },
        }
        SlngCmdExecutor.__init__(self, instance_parameters)
        SlngProcessRunner.__init__(self, instance_parameters)
        SlngConsoleHandler.__init__(self, instance_parameters)

    def start(self, syslog_ng_config, external_tool=None, expected_run=True):
        # syslog_ng_config.write_config_content()

        # exit_code = self.slng_executor(cmd_name="syntax_check").get_exit_code()
        # exit_code check

        if external_tool:
            process = self.slng_start_behind(parent_cmd_name=external_tool).get_process()
        process = self.slng_process_runner(cmd_name="start").get_process()

        # self.wait_for_console_message(self.start_message)
        # self.wait_for_start_message()
        # self.syslog_ng_ctl.wait_for_control_socket_start()

        # exit_code = self.slng_executor(cmd_name="syntax_check").get_exit_code()
        # print("Ez jott vissza: %s" % exit_code)

        # command = self.slng_process_runner(cmd_name="start").get_command()
        # print("Ez jott vissza2: %s" % command)

        # command = self.slng_start_behind(parent_cmd_name="strace").get_command()
        # print("Ez jott vissza3: %s" % command)

    def reload(self):
        pass

    def stop(self):
        pass



slng = SyslogNg()
slng.start()