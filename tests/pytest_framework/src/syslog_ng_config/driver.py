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

from src.syslog_ng_config.driver_message_handler import DriverMessageHandler
from src.syslog_ng_config.driver_option_handler import DriverOptionHandler
from src.syslog_ng_config.driver_stats_handler import DriverStatsHandler

class Driver(object):
    def __init__(self, logger_factory, instance_parameters, config_tree):
        self.config_tree = config_tree
        self.driver_message_handler = DriverMessageHandler()
        self.driver_option_handler = DriverOptionHandler(self.config_tree)
        self.driver_stats_handler = DriverStatsHandler(logger_factory, instance_parameters, self.config_tree)

    def generate_output_message(self):
        self.driver_message_handler.generate_output_message()

    def generate_default_output_message(self):
        self.driver_message_handler.generate_default_output_message()

    def add_options(self, options):
        self.driver_option_handler.add_options(options)

    def update_options(self, options):
        self.driver_option_handler.update_options(options)

    def remove_options(self, options):
        self.driver_option_handler.remove_options(options)

    def set_file_path_mandatory_option(self, options, mandatory_option_name, file_path_prefix, working_dir):
        self.driver_option_handler.set_file_path_mandatory_option(options, mandatory_option_name, file_path_prefix, working_dir)

    def get_stats_counters(self):
        return self.driver_stats_handler.get_stats_counters()

    def get_query_counters(self):
        return self.driver_stats_handler.get_query_counters()
