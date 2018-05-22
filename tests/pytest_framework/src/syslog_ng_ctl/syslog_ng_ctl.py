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

from src.syslog_ng_ctl.syslog_ng_ctl_as_command import SyslogNgCtlAsCommand
from src.syslog_ng_ctl.syslog_ng_ctl_counters import SyslogNgCtlCounters

class SyslogNgCtl(object):
    def __init__(self, logger_factory, instance_parameters):
        self.syslog_ng_ctl_as_command = SyslogNgCtlAsCommand(logger_factory, instance_parameters)
        self.syslog_ng_ctl_counters = SyslogNgCtlCounters(logger_factory, self.syslog_ng_ctl_as_command)

    def reload(self):
        return self.syslog_ng_ctl_as_command.reload()

    def stop(self):
        return self.syslog_ng_ctl_as_command.stop()

    def stats(self, reset=None):
        return self.syslog_ng_ctl_as_command.stats(reset)

    def query_get(self, query_pattern="*", query_sum=None, reset=None):
        return self.syslog_ng_ctl_as_command.query_get(query_pattern, query_sum, reset)

    def wait_for_control_socket_alive(self):
        return self.syslog_ng_ctl_as_command.wait_for_control_socket_alive()

    def wait_for_control_socket_stopped(self):
        return self.syslog_ng_ctl_as_command.wait_for_control_socket_stopped()

    def get_stats_counters(self, stats_component, stats_id, stats_instance, stats_state):
        return self.syslog_ng_ctl_counters.get_stats_counters(stats_component, stats_id, stats_instance, stats_state)

    def get_stats_counter(self, stats_component, stats_id, stats_instance, stats_state, stats_type):
        return self.syslog_ng_ctl_counters.get_stats_counter(stats_component, stats_id, stats_instance, stats_state, stats_type)

    def get_query_counters(self, query_component, query_id, query_instance):
        return self.syslog_ng_ctl_counters.get_query_counters(query_component, query_id, query_instance)

    def get_query_counter(self, query_component, query_id, query_instance, query_type):
        return self.syslog_ng_ctl_counters.get_query_counter(query_component, query_id, query_instance, query_type)
