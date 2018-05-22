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

from src.common.blocking import wait_until_false, wait_until_true
from src.syslog_ng_ctl.syslog_ng_ctl_executor import SyslogNgCtlExecutor

class SyslogNgCtlAsCommand(object):
    def __init__(self, logger_factory, instance_parameters):
        self.syslog_ng_ctl_executor = SyslogNgCtlExecutor(logger_factory, instance_parameters)

    def reload(self):
        return self.syslog_ng_ctl_executor.run_command(command_short_name="reload", command=["reload"])

    def stop(self):
        return self.syslog_ng_ctl_executor.run_command(command_short_name="stop", command=["stop"])

    def reopen(self):
        return self.syslog_ng_ctl_executor.run_command(command_short_name="reopen", command=["reopen"])

    def stats(self, reset):
        ctl_stats_command = self.syslog_ng_ctl_executor.construct_ctl_stats_command(reset=reset)
        return self.syslog_ng_ctl_executor.run_command(command_short_name="stats", command=ctl_stats_command)

    def query_get(self, query_pattern, query_sum, reset):
        ctl_query_command = self.syslog_ng_ctl_executor.construct_ctl_query_get_command(query_pattern, query_sum, reset)
        return self.syslog_ng_ctl_executor.run_command(command_short_name="query_get", command=ctl_query_command)

    def query_list(self, query_pattern="*"):
        ctl_query_command = self.syslog_ng_ctl_executor.construct_ctl_query_list_command(query_pattern)
        return self.syslog_ng_ctl_executor.run_command(command_short_name="query_list", command=ctl_query_command)

    def show_license_info(self, json=None):
        ctl_show_license_info_command = self.syslog_ng_ctl_executor.construct_ctl_show_license_info_command(json=json)
        return self.syslog_ng_ctl_executor.run_command(command_short_name="show_license_info", command=ctl_show_license_info_command)

    def credentials_add(self, credentials_id=None, secret=None):
        ctl_credentials_command = self.syslog_ng_ctl_executor.construct_ctl_credentials_add_command(credentials_id=credentials_id, secret=secret)
        return self.syslog_ng_ctl_executor.run_command(command_short_name="credentials_add", command=ctl_credentials_command)

    def credentials_status(self):
        ctl_credentials_command = self.syslog_ng_ctl_executor.construct_ctl_credentials_status_command()
        return self.syslog_ng_ctl_executor.run_command(command_short_name="credentials_status", command=ctl_credentials_command)

    def is_control_socket_alive(self):
        return self.stats(reset=False)['exit_code'] == 0

    def wait_for_control_socket_alive(self):
        return wait_until_true(self.is_control_socket_alive)

    def wait_for_control_socket_stopped(self):
        return wait_until_false(self.is_control_socket_alive)
