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

from src.common.find_in_content import grep_in_content
class SyslogNgCtlCounters(object):
    def __init__(self, logger_factory, syslog_ng_ctl_as_command):
        self.logger = logger_factory.create_logger("SyslogNgCtlCounters")
        self.syslog_ng_ctl_as_command = syslog_ng_ctl_as_command
        self.stats_counter_types = ["processed", "written", "queued", "dropped", "memory_usage"]
        self.query_counter_types = ["processed", "written", "queued", "dropped", "memory_usage"]
        self.delimiters = {
            "stats_item": ";",
            "stats_counter": ";",
            "query_item": ".",
            "query_counter": "=",
        }

    def get_stats_counters(self, stats_component, stats_id, stats_instance, stats_state):
        found_stats_counters = {}
        for counter_type in self.stats_counter_types:
            counter = self.get_stats_counter(stats_component, stats_id, stats_instance, stats_state, counter_type)
            if counter is not None:
                found_stats_counters.update({counter_type: counter})
        return found_stats_counters

    def get_stats_counter(self, stats_component, stats_id, stats_instance, stats_state, stats_type):
        actual_stats = self.syslog_ng_ctl_as_command.stats(reset=None)['stdout']
        formatted_stats_line = self.format_stats_line(stats_component, stats_id, stats_instance, stats_state, stats_type)
        found_stats_line = grep_in_content(regexp=formatted_stats_line, content=actual_stats)
        if found_stats_line:
            counter = int(found_stats_line.split(self.delimiters['stats_counter'])[-1].replace("\n", ""))
            return counter
        return None

    def format_stats_line(self, stats_component, stats_id, stats_instance, stats_state, stats_type):
        item_delimiter = self.delimiters['stats_item']
        stats_line = "{}{}".format(stats_component, item_delimiter)
        stats_line += "{}.*{}".format(stats_id, item_delimiter) # config_id#counter for driver
        stats_line += "{}{}".format(stats_instance, item_delimiter)
        stats_line += "{}{}".format(stats_state, item_delimiter)
        stats_line += "{}{}".format(stats_type, item_delimiter)
        return stats_line

    def get_query_counters(self, query_component, query_id, query_instance):
        found_query_counters = {}
        for counter_type in self.query_counter_types:
            counter = self.get_query_counter(query_component, query_id, query_instance, counter_type)
            if counter is not None:
                found_query_counters.update({counter_type: counter})
        return found_query_counters

    def get_query_counter(self, query_component, query_id, query_instance, query_type):
        actual_query = self.syslog_ng_ctl_as_command.query_get(query_pattern="*", query_sum=None, reset=None)['stdout']
        formatted_query_line = self.format_query_line(query_component, query_id, query_instance, query_type)
        found_query_line = grep_in_content(regexp=formatted_query_line, content=actual_query)
        if found_query_line:
            counter = int(found_query_line.split(self.delimiters['query_counter'])[-1].replace("\n", ""))
            return counter
        return None

    def format_query_line(self, query_component, query_id, query_instance, query_type):
        item_delimiter = self.delimiters['query_item']
        query_line = "{}{}".format(query_component, item_delimiter)
        query_line += "{}.*{}".format(query_id, item_delimiter) # config_id#counter for driver
        query_line += "{}{}".format(query_instance, item_delimiter)
        query_line += "{}{}".format(query_type, item_delimiter)
        return query_line
