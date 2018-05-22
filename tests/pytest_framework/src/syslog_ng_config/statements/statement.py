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
from src.common.random_id import RandomId
from src.syslog_ng_config.config_tree import ConfigTree
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl

class Statement(ConfigTree):
    def __init__(self, logger_factory, instance_parameters, empty_driver_content):
        super(Statement, self).__init__(empty_driver_content)
        self.empty_driver_content = empty_driver_content
        self.mandatory_option_value = None
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        self.native_driver_io = None

    # build statement
    def build_statement(self, build_status, syslog_ng_config, root_node_name, options):
        if build_status:
            self.build(syslog_ng_config, root_node_name, options)
        else:
            self.build_driver_without_parent(syslog_ng_config, options)

    # Driver specific option setup
    def set_file_path_mandatory_option(self, options, file_path_prefix, working_dir):
        mandatory_option_name = self.empty_driver_content['mandatory_option_name']
        if options is None:
            options = {}
        if not mandatory_option_name in options.keys():
            random_id = RandomId(use_static_seed=False).get_unique_id()
            self.mandatory_option_value = construct_path(working_dir, "{}_{}.log".format(file_path_prefix, random_id))
        else:
            self.mandatory_option_value = construct_path(working_dir, "{}_{}.log".format(file_path_prefix, options[mandatory_option_name]))

        options.update({mandatory_option_name: self.mandatory_option_value})
        return options

    def update_file_path_mandatory_option(self, options, file_path_prefix, working_dir):
        mandatory_option_name = self.empty_driver_content['mandatory_option_name']
        if mandatory_option_name in options.keys():
            self.reset_native_driver_io()
            self.mandatory_option_value = construct_path(working_dir, "{}_{}.log".format(file_path_prefix, options[mandatory_option_name]))
            options.update({mandatory_option_name: self.mandatory_option_value})
        return options

    def reset_native_driver_io(self):
        self.native_driver_io = False

    def get_counters(self):
        statement_short_name = self.empty_driver_content["statement_short_name"]
        driver_name = self.empty_driver_content["driver_name"]
        component = "{}.{}".format(statement_short_name, driver_name)
        stats_counters = self.syslog_ng_ctl.get_stats_counters(
            stats_component=component,
            stats_id=self.stmt_id,
            stats_instance=self.mandatory_option_value,
            stats_state="a"
        )
        query_counters = self.syslog_ng_ctl.get_query_counters(
            query_component=component,
            query_id=self.stmt_id,
            query_instance=self.mandatory_option_value
        )
        assert stats_counters == query_counters
        return query_counters
