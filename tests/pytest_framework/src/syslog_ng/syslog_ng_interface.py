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

from src.syslog_ng.command_executor import SlngCommandExecutor
from src.syslog_ng.process_executor import SlngProcessExecutor
from src.syslog_ng.console_handler import SlngConsoleHandler
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl


class SyslogNgInterface(object):

    def __init__(self, logger_factory, instance_parameters):
        self.slng_command_executor = SlngCommandExecutor(logger_factory, instance_parameters)
        self.slng_process_executor = SlngProcessExecutor(logger_factory, instance_parameters)
        self.slng_console_handler = SlngConsoleHandler(logger_factory)
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        self.found_core_file = False
        self.stderr_file = None

    def save_stderr_file(self, stderr_file):
        self.stderr_file = stderr_file

    def syslog_ng_execute_command(self, cmd_reference):
        self.save_stderr_file(self.slng_command_executor.slng_commands[cmd_reference]["stderr"])
        return self.slng_command_executor.slng_executor(cmd_reference)

    def is_core_file_exist(self):
        self.found_core_file = self.slng_command_executor.is_core_file_exist()
        return self.found_core_file

    def syslog_ng_process_start_behind(self, external_tool):
        self.save_stderr_file(self.slng_process_executor.process_start_command_args[external_tool]["stderr"])
        return self.slng_process_executor.slng_process_start_behind(external_tool=external_tool)

    def syslog_ng_process_start(self):
        self.save_stderr_file(self.slng_process_executor.process_start_command_args["start"]["stderr"])
        return self.slng_process_executor.slng_process_start()

    def syslog_ng_process_reload(self):
        return self.slng_process_executor.slng_process_reload()

    def syslog_ng_process_stop(self):
        return self.slng_process_executor.slng_process_stop()

    def syslog_ng_is_running(self):
        return self.slng_process_executor.slng_is_running()

    def wait_for_start_message(self):
        return self.slng_console_handler.wait_for_start_message(self.stderr_file)

    def wait_for_reload_message(self):
        return self.slng_console_handler.wait_for_reload_message(self.stderr_file)

    def wait_for_stop_message(self):
        return self.slng_console_handler.wait_for_stop_message(self.stderr_file)

    def wait_for_control_socket_start(self):
        return self.syslog_ng_ctl.wait_for_control_socket_start()

    def wait_for_control_socket_stop(self):
        return self.syslog_ng_ctl.wait_for_control_socket_stop()

    def dump_console_log(self):
        return self.slng_console_handler.dump_console_log(self.stderr_file)
