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

from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl

class DriverStatsHandler(object):
    def __init__(self, logger_factory, instance_parameters, config_tree):
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        self.config_tree = config_tree

    def get_stats_counters(self):
        statement_short_name = self.config_tree.driver_node["statement_short_name"]
        driver_name = self.config_tree.driver_node["driver_name"]
        statement_id = self.config_tree.statement_id
        mandatory_option_value = self.config_tree.get_mandatory_option_value()
        stats_line_regexp_without_counter = self.syslog_ng_ctl.get_formatted_stats_line(
            config_component="{}.{}".format(statement_short_name, driver_name),
            config_item_id=statement_id,
            config_item_instance=mandatory_option_value,
            stats_type="stats",
        )
        return self.syslog_ng_ctl.get_driver_based_stats_counters(stats_line_regexp_without_counter, "stats")

    def get_query_counters(self):
        statement_short_name = self.config_tree.driver_node["statement_short_name"]
        driver_name = self.config_tree.driver_node["driver_name"]
        statement_id = self.config_tree.statement_id
        mandatory_option_value = self.config_tree.get_mandatory_option_value()
        query_line_regexp_without_counter = self.syslog_ng_ctl.get_formatted_stats_line(
            config_component="{}.{}".format(statement_short_name, driver_name),
            config_item_id=statement_id,
            config_item_instance=mandatory_option_value,
            stats_type="query",
        )
        return self.syslog_ng_ctl.get_driver_based_stats_counters(query_line_regexp_without_counter, "query")
