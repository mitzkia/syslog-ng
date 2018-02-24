import os
import logging

from src.common.blocking import wait_until_false, wait_until_true
from src.driver_io.file_based.file import File
from src.driver_io.file_based.filewaitforevent import FileWaitForEvent
from src.executor.executor_interface import ExecutorInterface
from src.syslog_ng_ctl.syslogngctl import SyslogNgCtl


class SyslogNg(object):
    def __init__(self, logger_factory, syslog_ng_parameters_object, instance_name):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SyslogNg")
        self.instance_parameters = syslog_ng_parameters_object.set_instance_parameters(instance_name)
        self.working_dir = syslog_ng_parameters_object.working_dir
        self.syslog_ng_binary_path = self.instance_parameters['binary_file_paths']['syslog_ng_binary']

        self.external_commands = {
            "strace": ["strace", "-s", "8888", "-ff", "-o", os.path.join(self.working_dir, 'strace.log')],
            "valgrind": ["valgrind", "--show-leak-kinds=all", "--track-origins=yes", "--tool=memcheck", "--leak-check=full", "--log-driver_file={}".format((os.path.join(self.working_dir, 'valgrind.log')))],
            "perf": ["perf", "record", "-g", "-v", "-s", "-F", "99", "--output={}".format(os.path.join(self.working_dir, 'perf.log'))],
            "gdb": [""]
        }
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, self.instance_parameters)
        self.executor = ExecutorInterface(logger_factory)

        self.expected_run = None
        self.external_tool = None
        self.syslog_ng_process = None
        self.syslog_ng_pid = None
        self.registered_start = 0
        self.registered_stop = 0
        self.registered_reload = 0
        self.syslog_ng_start_message = ["syslog-ng starting up;"]
        self.syslog_ng_stop_message = ["syslog-ng shutting down"]
        self.syslog_ng_reload_messages = [
            "New configuration initialized",
            "Configuration reload request received, reloading configuration",
            "Configuration reload finished"
        ]

    def start(self, syslog_ng_config, external_tool=None, expected_run=True):
        self.logger.info("syslog-ng start phase 1")
        self.expected_run = expected_run
        syslog_ng_config.write_config_content(self.instance_parameters['file_paths']['config_path'])
        self.logger.info("syslog-ng start phase 2: syslog-ng config was written")
        self.run_syntax_check_on_config()
        self.run_syslog_ng_process(external_tool=external_tool)

    def stop(self):
        self.logger.info("syslog-ng stop phase 1")
        self.handle_if_syslog_ng_already_killed()
        self.stop_syslog_ng_process()

    def reload(self, syslog_ng_config):
        self.logger.info("syslog-ng reload phase 1")
        self.handle_if_syslog_ng_already_killed()
        syslog_ng_config.write_config_content(self.instance_parameters['file_paths']['config_path'])
        self.logger.info("syslog-ng reload phase 2: syslog-ng config was written")
        self.reload_syslog_ng_process()

    def restart(self, syslog_ng_config):
        self.stop()
        self.start(syslog_ng_config)

# Low level functions
    def run_syntax_check_on_config(self):
        exit_code = self.executor.execute_command(command=self.get_syslog_ng_start_command(syntax_check=True))[0]
        self.handle_config_syntax_check_result(exit_code)

    def run_syslog_ng_process(self, external_tool=None):
        self.syslog_ng_process = self.executor.start_process(
            command=self.get_syslog_ng_start_command(syntax_check=False),
            stdout=self.instance_parameters['file_paths']['stdout_fd'],
            stderr=self.instance_parameters['file_paths']['stderr_fd'],
        )
        if not external_tool:
            syslog_ng_start_result = self.wait_for_syslog_ng_start()
            self.handle_syslog_ng_start_process_result(syslog_ng_start_result=syslog_ng_start_result)
        else:
            self.syslog_ng_ctl.wait_for_control_socket_start()
            wait_until_true(self.executor.is_pid_in_process_list, self.get_syslog_ng_pid(), monitoring_time=1)

    def handle_if_syslog_ng_already_killed(self):
        if not self.executor.is_pid_in_process_list(self.get_syslog_ng_pid()):
            self.is_core_file_exist()
            raise Exception("syslog-ng was killed outside of syslog-ng handler. last pid: [{}]".format(self.get_syslog_ng_pid()))

    def stop_syslog_ng_process(self):
        self.executor.stop_process(process=self.get_syslog_ng_process())
        self.wait_for_syslog_ng_stop()
        self.handle_syslog_ng_stop_process_result()

    def reload_syslog_ng_process(self):
        self.executor.reload_process(process=self.get_syslog_ng_process())
        self.wait_for_syslog_ng_reload()
        self.handle_syslog_ng_reload_process_result()

    def get_syslog_ng_start_command(self, syntax_check=None):
        start_command = "{} ".format(self.syslog_ng_binary_path)
        start_command += "-Fedtv --no-caps --enable-core "
        start_command += "-f {} ".format(self.instance_parameters['file_paths']['config_path'])
        start_command += "-R {} ".format(self.instance_parameters['file_paths']['persist_path'])
        start_command += "-p {} ".format(self.instance_parameters['file_paths']['pid_path'])
        start_command += "-c {} ".format(self.instance_parameters['file_paths']['control_socket_path'])
        if syntax_check:
            start_command += "--syntax-only "
        return start_command

    def handle_config_syntax_check_result(self, exit_code):
        if self.expected_run and (exit_code != 0):
            raise Exception("syslog-ng start phase 3: syslog-ng can not start with config")
        elif not self.expected_run and (exit_code != 0):
            self.logger.info("syslog-ng start phase 3: syslog-ng can not started, but this was the expected behaviour")
        else:
            self.logger.info("syslog-ng start phase 3: syslog-ng can started with config")

    def handle_syslog_ng_start_process_result(self, syslog_ng_start_result):
        if not self.expected_run and (not syslog_ng_start_result):
            self.logger.info("syslog-ng start phase 5: syslog-ng can not started, but this was the expected behaviour")
        elif (not self.expected_run) and syslog_ng_start_result:
            raise Exception("syslog-ng start phase 5: the expected behaviour was syslog-ng can not started, but it started successfully")
        elif (not syslog_ng_start_result) or (not self.executor.is_pid_in_process_list(pid=self.get_syslog_ng_pid())):
            raise Exception("syslog-ng start phase 5: syslog-ng can not started")
        else:
            self.logger.info("syslog-ng start phase 5: syslog-ng started successfully")

    def handle_syslog_ng_stop_process_result(self):
        if self.executor.is_pid_in_process_list(pid=self.get_syslog_ng_pid()):
            raise Exception("syslog-ng stop phase 3: syslog-ng can not stopped successfully")
        else:
            self.syslog_ng_process = None
            self.syslog_ng_pid = None
            self.logger.info("syslog-ng stop phase 3: syslog-ng stopped successfully")

    def handle_syslog_ng_reload_process_result(self):
        if not self.executor.is_pid_in_process_list(pid=self.get_syslog_ng_pid()):
            raise Exception("syslog-ng stop phase 4: syslog-ng can not reloaded successfully")
        else:
            self.logger.info("syslog-ng stop phase 4: syslog-ng reloaded successfully")

    def wait_for_syslog_ng_start(self):
        control_socket_alive = False
        pid_in_process_list = False

        self.registered_start += 1
        start_message_arrived = self.wait_for_console_messages(messages=self.syslog_ng_start_message, expected_occurance=self.registered_start)
        self.logger.write_message_based_on_value(message="syslog-ng start phase 4: syslog-ng start message arrived", value=start_message_arrived, loglevel=logging.INFO)
        if start_message_arrived:
            control_socket_alive = self.syslog_ng_ctl.wait_for_control_socket_start()
            self.logger.write_message_based_on_value(message="syslog-ng start phase 4: syslog-ng control socket alive", value=control_socket_alive, loglevel=logging.INFO)
        if control_socket_alive:
            pid_in_process_list = wait_until_true(self.executor.is_pid_in_process_list, self.get_syslog_ng_pid(), monitoring_time=1)
            self.logger.write_message_based_on_value(message="syslog-ng start phase 4: syslog-ng's pid is in process list", value=pid_in_process_list, loglevel=logging.INFO)
        self.is_core_file_exist()
        return start_message_arrived and control_socket_alive and pid_in_process_list

    def wait_for_syslog_ng_stop(self):
        control_socket_not_alive = False
        pid_not_in_process_list = False

        self.registered_stop += 1
        stop_message_arrived = self.wait_for_console_messages(messages=self.syslog_ng_stop_message, expected_occurance=self.registered_stop)
        self.logger.write_message_based_on_value(message="syslog-ng stop phase 2: syslog-ng stop message arrived", value=stop_message_arrived, loglevel=logging.INFO)
        if stop_message_arrived:
            control_socket_not_alive = self.syslog_ng_ctl.wait_for_control_socket_stop()
            self.logger.write_message_based_on_value(message="syslog-ng stop phase 2: syslog-ng control socket not alive", value=control_socket_not_alive, loglevel=logging.INFO)
        if control_socket_not_alive:
            pid_not_in_process_list = wait_until_false(self.executor.is_pid_in_process_list, self.get_syslog_ng_pid())
            self.logger.write_message_based_on_value(message="syslog-ng stop phase 2: syslog-ng's pid is not in process list", value=pid_not_in_process_list, loglevel=logging.INFO)
        self.is_core_file_exist()
        return stop_message_arrived and control_socket_not_alive and pid_not_in_process_list

    def wait_for_syslog_ng_reload(self):
        control_socket_alive = False
        pid_in_process_list = False

        self.registered_reload += 1
        reload_message_arrived = self.wait_for_console_messages(messages=self.syslog_ng_reload_messages, expected_occurance=self.registered_reload)
        self.logger.write_message_based_on_value(message="syslog-ng reload phase 3: syslog-ng reload message arrived", value=reload_message_arrived, loglevel=logging.INFO)
        if reload_message_arrived:
            control_socket_alive = self.syslog_ng_ctl.wait_for_control_socket_start()
            self.logger.write_message_based_on_value(message="syslog-ng stop phase 3: syslog-ng control socket alive", value=control_socket_alive, loglevel=logging.INFO)
        if control_socket_alive:
            pid_in_process_list = wait_until_true(self.executor.is_pid_in_process_list, self.get_syslog_ng_pid(), monitoring_time=1)
            self.logger.write_message_based_on_value(message="syslog-ng stop phase 3: syslog-ng's pid is in process list", value=pid_in_process_list, loglevel=logging.INFO)
        self.is_core_file_exist()
        return reload_message_arrived and control_socket_alive and pid_in_process_list

    def wait_for_console_messages(self, messages, expected_occurance=1):
        std_error_file = FileWaitForEvent(self.logger_factory, self.instance_parameters['file_paths']['stderr_path'])
        result = []
        for message in messages:
            result.append(std_error_file.wait_for_message(expected_message=message, expected_occurance=expected_occurance))
        return all(result)

    def is_core_file_exist(self):
        for syslog_ng_core_file in [os.path.join(os.getcwd(), "core*")]:
            if File(self.logger_factory, syslog_ng_core_file).is_wildcard_file_exist():
                core_backtrace_path = os.path.join(self.working_dir, "core_backtrace.txt")
                gdb_command = ['gdb', '--core', syslog_ng_core_file, self.syslog_ng_binary_path, '-ex', 'bt full', '--batch']
                backtrace_output = self.executor.execute_command(command=gdb_command)[1]
                File(self.logger_factory, core_backtrace_path).write(backtrace_output, 'w')
                File(self.logger_factory, syslog_ng_core_file).move_file("{}/".format(self.working_dir))
                self.syslog_ng_process = None
                self.syslog_ng_pid = None
                raise Exception("core file detected")
        return True

    def get_syslog_ng_pid(self):
        return self.syslog_ng_process.pid

    def get_syslog_ng_process(self):
        return self.syslog_ng_process

    def dump_config(self):
        File(self.logger_factory, self.instance_parameters['file_paths']['config_path']).dump_content()

    def dump_console_log(self):
        File(self.logger_factory, self.instance_parameters['file_paths']['stderr_path']).dump_content()
