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
from src.syslog_ng_ctl.command_executor import CtlCommandExecutor
from src.common.find_in_content import grep_pattern_in_content


class SyslogNgCtl(CtlCommandExecutor):
    def __init__(self, logger_factory, instance_parameters):
        CtlCommandExecutor.__init__(self, logger_factory, instance_parameters)
        self.logger = logger_factory.create_logger("SyslogNgCtl")
        self.stats_counters = ["processed", "written", "queued", "dropped", "memory_usage"]

    def stats(self):
        return self.slng_ctl_executor(cmd_name="stats").get_stdout()

    def stats_reset(self):
        return self.slng_ctl_executor(cmd_name="stats_reset").get_all()

    def query_get(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_get", query_pattern=pattern).get_stdout()

    def query_get_sum(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_get_sum", query_pattern=pattern).get_all()

    def query_list(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_list", query_pattern=pattern).get_all()

    def query_reset(self, pattern="*"):
        return self.slng_ctl_executor(cmd_name="query_reset", query_pattern=pattern).get_all()

    def stop(self):
        return self.slng_ctl_executor(cmd_name="stop").get_all()

    def reload(self):
        return self.slng_ctl_executor(cmd_name="reload").get_all()

    def reopen(self):
        return self.slng_ctl_executor(cmd_name="reopen").get_all()

    def is_control_socket_alive(self):
        return self.slng_ctl_executor(cmd_name="stats").get_exit_code() == 0

    def wait_for_control_socket_start(self):
        return wait_until_true(self.is_control_socket_alive)

    def wait_for_control_socket_stop(self):
        return wait_until_false(self.is_control_socket_alive)

    @staticmethod
    def get_stats_item_delimiter_by_type(stats_type):
        if stats_type == "query":
            return "."
        elif stats_type == "stats":
            return ";"
        else:
            raise ValueError("Unknown stats type")

    @staticmethod
    def get_stats_counter_delimiter_by_type(stats_type):
        if stats_type == "query":
            return "="
        elif stats_type == "stats":
            return ";"
        else:
            raise ValueError("Unknown stats type")

    def get_stats_by_type(self, stats_type):
        if stats_type == "stats":
            return self.stats()
        elif stats_type == "query":
            return self.query_get()
        else:
            raise ValueError("Unknown stats type")

    def get_formatted_stats_line(self, config_component, config_item_id, config_item_instance, stats_type):
        item_delimiter = self.get_stats_item_delimiter_by_type(stats_type)
        stats_line = "{}{}".format(config_component, item_delimiter)
        stats_line += "{}#[0-9]*{}".format(config_item_id, item_delimiter) # config_id#counter for driver
        stats_line += "{}{}".format(config_item_instance, item_delimiter)
        if stats_type == "stats":
            state_type = "a"
            stats_line += "{}{}".format(state_type, item_delimiter)
        return stats_line

    def get_driver_based_stats_counters(self, stats_line_regexp_without_counter, stats_type):
        actual_stats = self.get_stats_by_type(stats_type)
        counter_delimiter = self.get_stats_counter_delimiter_by_type(stats_type)
        found_stats_counters = {}
        for counter_type in self.stats_counters:
            stats_line_regexp_with_counter = stats_line_regexp_without_counter+counter_type
            found_pattern = grep_pattern_in_content(pattern=stats_line_regexp_with_counter, content=actual_stats)
            if found_pattern:
                stats_counter_value = int(found_pattern.split(counter_delimiter)[-1].replace("\n", ""))
                found_stats_counters.update({counter_type: stats_counter_value})
        return found_stats_counters
