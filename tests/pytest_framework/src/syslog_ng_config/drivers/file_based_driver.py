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

import os
from src.common.random import Random
from src.syslog_ng_config.drivers.driver_base import DriverBase
from src.driver_io.file_based.file_interface import FileInterface
from src.message.message_interface import MessageInterface
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl


class FileBasedDriver(DriverBase):

    def __init__(self, statement, driver, option_setter, logger_factory, instance_parameters):
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        DriverBase.__init__(self, statement, driver, option_setter)
        self.logger_factory = logger_factory
        self.working_dir = instance_parameters["dir_paths"]["working_dir"]
        # renderer uses this values
        if self.driver.node_name in ["file", "pipe", "program"]:
            self.driver.created_node["mandatory_option_names"] = ["file_path"]
        elif self.driver.node_name == "wildcard_file":
            self.driver.created_node["mandatory_option_names"] = ["base_dir", "file_pattern"]
        else:
            print("Unknown driver: %s" % self.driver.node_name)
        self.mandatory_option_value = None  # needed on generating stats values
        self.random_id = Random(use_static_seed=False).get_unique_id()

    # Message, this part is uniq for FileBasedDriver, can not put into DriverBase
    def generate_default_output_message(self, counter=1):
        return MessageInterface(self.logger_factory).construct_bsd_messages({"priority": "skip"}, counter)

    def generate_output_message(
        self, message="test message - árvíztűrő tükörfúrógép", message_header_fields=None, counter=1
    ):
        message_field = {"message": message}
        if message_header_fields:
            message_header_fields = {**message_header_fields, **{"priority": "skip"}}
        else:
            message_header_fields = {**{"priority": "skip"}}
        message_parts = {**message_field, **message_header_fields}
        return MessageInterface(self.logger_factory).construct_bsd_messages(message_parts, counter)

    # DriverIO, this part is uses FileBasedDriver specific variables, can not put into DriverBase
    def write(self, message, normalize_line_endings=True):
        return FileInterface(self.logger_factory).write_content(
            self.mandatory_option_value, content=message, normalize_line_endings=normalize_line_endings
        )

    def read(self, counter=1):
        return FileInterface(self.logger_factory).read_content(
            self.mandatory_option_value, expected_message_counter=counter
        )

    def read_messages(self, expected_message_counter=2):
        return self.read(expected_message_counter)

    # Options, this part is uses FileBasedDriver specific variables, can not put into DriverBase
    def add_options(self, driver_node, options=None):
        if not options:
            options = {}
        options.update(self.set_mandatory_options(options))
        self.option_setter.add_options(driver_node["driver_options"], options)

    def set_mandatory_options(self, options):
        mandatory_options = {}
        for mandatory_option_name in self.driver.created_node["mandatory_option_names"]:
            if mandatory_option_name == "file_path":
                if mandatory_option_name in options.keys():
                    option_value = os.path.join(
                        self.working_dir,
                        "{}_{}_{}.log".format(options[mandatory_option_name], self.driver.node_name, self.random_id),
                    )
                else:
                    option_value = os.path.join(
                        self.working_dir, "{}_{}.log".format(self.driver.node_name, self.random_id)
                    )
            else:
                raise ValueError("Unknown mandatory option name")
            mandatory_options.update({mandatory_option_name: option_value})
        self.mandatory_option_value = option_value
        return mandatory_options

    def update_options(self, options):
        if self.is_mandatory_option_exist(options):
            options.update(self.set_mandatory_options(options))
        self.option_setter.add_options(self.option_setter.root_node, options)

    def remove_options(self, options):
        self.option_setter.remove_options(options)

    def is_mandatory_option_exist(self, options):
        return len(set(options).intersection(self.driver.created_node["mandatory_option_names"])) != 0

    # Stats, this part is uses FileBasedDriver specific variables, can not put into DriverBase
    def get_stats_counters(self):
        stats_line_regexp_without_counter = self.syslog_ng_ctl.get_formatted_stats_line(
            config_component="{}.{}".format(self.statement.node_short_name, self.driver.node_name),
            config_item_id=self.statement.node_id,
            config_item_instance=self.mandatory_option_value,
            stats_type="stats",
        )
        return self.syslog_ng_ctl.get_driver_based_stats_counters(stats_line_regexp_without_counter, "stats")

    def get_query_counters(self):
        query_line_regexp_without_counter = self.syslog_ng_ctl.get_formatted_stats_line(
            config_component="{}.{}".format(self.statement.node_short_name, self.driver.node_name),
            config_item_id=self.statement.node_id,
            config_item_instance=self.mandatory_option_value,
            stats_type="query",
        )
        return self.syslog_ng_ctl.get_driver_based_stats_counters(query_line_regexp_without_counter, "query")
