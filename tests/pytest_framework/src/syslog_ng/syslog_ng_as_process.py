#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2018 Balabit
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# As an additional exemption you are allowed to compile & link against the
# OpenSSL libraries as published by the OpenSSL project. See the file
# COPYING for details.
#
#############################################################################

from pathlib2 import Path
from src.syslog_ng.syslog_ng_executor import SyslogNgExecutor
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl
from src.driver_io.file.file import File

class SyslogNgAsProcess(object):
    def __init__(self, logger_factory, instance_parameters, console_log):
        self.logger_factory = logger_factory
        self.syslog_ng_console_log = console_log
        self.logger = logger_factory.create_logger("SyslogNgAsProcess")
        self.working_dir = instance_parameters.get_working_dir()
        self.syslog_ng_executor = SyslogNgExecutor(logger_factory, instance_parameters)
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        self.stderr_path = None
        self.process = None
        self.core_file_exist = None
        self.config = None

    def start(self, config, external_tool, expected_run):
        self.logger.info("Beginning of syslog-ng start")
        self.prepare_config(config)

        # syntax check
        result = self.syslog_ng_executor.run_command(command_short_name="syntax_only")
        if (not expected_run) and (result['exit_code'] != 0):
            self.logger.info("syslog-ng can not started, but this was the expected behaviour")
            return None
        if expected_run and result['exit_code'] != 0:
            self.logger.error(result['stderr'])
            raise Exception("syslog-ng can not started")

        # effective start
        if external_tool:
            self.process, self.stderr_path = self.syslog_ng_executor.run_process_behind(process_short_name=external_tool)
        else:
            self.process, self.stderr_path = self.syslog_ng_executor.run_process(process_short_name="start")

        # wait for start and check start result
        if not self.syslog_ng_ctl.wait_for_control_socket_alive():
            self.error_handling()
            raise Exception("Control socket not alive")
        if not self.syslog_ng_console_log.wait_for_start_message(self.stderr_path):
            self.error_handling()
            raise Exception("Start message not arrived")
        self.logger.info("End of syslog-ng start")

    def reload(self, config):
        self.logger.info("Beginning of syslog-ng reload")
        self.prepare_config(config)

        # effective reload
        self.syslog_ng_ctl.reload()

        # wait for reload and check reload result
        if not self.syslog_ng_ctl.wait_for_control_socket_alive():
            self.error_handling()
            raise Exception("Control socket not alive")
        if not self.syslog_ng_console_log.wait_for_reload_message(self.stderr_path):
            self.error_handling()
            raise Exception("Reload message not arrived")
        self.logger.info("End of syslog-ng reload")

    def stop(self):
        self.logger.info("Beginning of syslog-ng stop")
        if self.process and not self.core_file_exist:

            # effective stop
            result = self.syslog_ng_ctl.stop()

            # wait for stop and check stop result
            if result["exit_code"] != 0:
                self.error_handling()
            if not self.syslog_ng_ctl.wait_for_control_socket_stopped():
                self.error_handling()
                raise Exception("Control socket still alive")
            if not self.syslog_ng_console_log.wait_for_stop_message(self.stderr_path):
                self.error_handling()
                raise Exception("Stop message not arrived")
            self.syslog_ng_console_log.check_for_unexpected_messages(self.stderr_path)
            self.process = None
            self.logger.info("End of syslog-ng stop")

    def get_process_info(self):
        return self.syslog_ng_executor.get_process_info()

    def prepare_config(self, config):
        if not config:
            config = self.config
        else:
            self.config = config
        config.write_config_content()

    def error_handling(self):
        self.syslog_ng_console_log.dump_stderr(self.stderr_path)
        self.check_core_file(self.process)

    def check_core_file(self, process):
        if process.wait(1) != 0:
            for core_file in Path('.').glob('*core*'):
                self.core_file_exist = True
                self.syslog_ng_executor.run_command(command_short_name="gdb-bt-full", core_file=str(core_file))
                File(self.logger_factory, core_file).move_file(self.working_dir)
                raise Exception("syslog-ng core file found and processed")
