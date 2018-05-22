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

from src.common.path_and_operations import construct_path
from src.executors.command_executor import CommandExecutor

class SyslogNgCtlExecutor(object):
    def __init__(self, logger_factory, instance_parameters):
        self.instance_parameters = instance_parameters
        self.working_dir = instance_parameters.get_working_dir()
        self.syslog_ng_control_tool_path = instance_parameters.get_syslog_ng_ctl_bin()
        self.syslog_ng_control_socket_path = instance_parameters.get_control_socket_path()
        self.command_executor = CommandExecutor(logger_factory)

    def run_command(self, command_short_name, command):
        return self.command_executor.run(
            command=self.construct_ctl_command(command),
            stdout_path=self.construct_std_file_path(command_short_name, "stdout"),
            stderr_path=self.construct_std_file_path(command_short_name, "stderr")
        )

    def construct_std_file_path(self, command_short_name, std_type):
        instance_name = self.instance_parameters.get_instance_name()
        return construct_path(self.working_dir, "syslog_ng_ctl_{}_{}_{}".format(instance_name, command_short_name, std_type))

    def construct_ctl_command(self, command):
        ctl_command = [self.syslog_ng_control_tool_path]
        ctl_command += command
        ctl_command.append("--control={}".format(self.syslog_ng_control_socket_path))
        return ctl_command

    @staticmethod
    def construct_ctl_stats_command(reset):
        stats_command = ["stats"]
        if reset:
            stats_command.append("--reset")
        return stats_command

    @staticmethod
    def construct_ctl_query_get_command(query_pattern, query_sum, reset):
        query_get_command = ["query", "get", query_pattern]
        if query_sum:
            query_get_command.append("--sum")
        if reset:
            query_get_command.append("--reset")
        return query_get_command

    @staticmethod
    def construct_ctl_query_list_command(query_pattern):
        query_list_command = ["query", "list", query_pattern]
        return query_list_command

    @staticmethod
    def construct_ctl_show_license_info_command(json):
        show_license_info_command = ["show-license-info"]
        if json:
            show_license_info_command.append("--json")
        return show_license_info_command

    @staticmethod
    def construct_ctl_credentials_add_command(credentials_id, secret):
        credentials_add_command = ["credentials", "add"]
        if credentials_id:
            credentials_add_command.append("--id={}".format(credentials_id))
        if secret:
            credentials_add_command.append("--secret={}".format(secret))
        return credentials_add_command

    @staticmethod
    def construct_ctl_credentials_status_command():
        credentials_status_command = ["credentials", "status"]
        return credentials_status_command
