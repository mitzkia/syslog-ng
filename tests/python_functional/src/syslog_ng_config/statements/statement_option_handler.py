#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2019 Balabit
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
from pathlib2 import Path

import src.testcase_parameters.testcase_parameters as tc_parameters
from src.common.random_id import get_unique_id


class StatementOptionHandler(object):
    def __init__(self, options, driver_direction=None):
        self.driver_direction = driver_direction

        self.general_options_and_values = options
        self.positional_options_and_values = {}

        self.mandatory_options = []
        self.driver_io_options = []
        self.positional_options = []

        self.known_positional_option_names = ["file_name"]

    def non_positional_options(self):
        return self.general_options_and_values

    def reload_options(self, options):
        self.general_options_and_values = options

    def register_option_list(self, option_list, mandatory=True, driver_io=True, positional=True):
        if mandatory:
            self.mandatory_options.extend(option_list)
        if driver_io:
            self.driver_io_options.extend(option_list)
        if positional:
            self.positional_options.extend(option_list)

    def register_mandatory_options(self, option_list):
        self.mandatory_options.extend(option_list)

    def register_driver_io_options(self, option_list):
        self.driver_io_options.extend(option_list)

    def register_positional_options(self, option_list):
        for option_name in option_list:
            if option_name not in self.known_positional_option_names:
                raise ValueError("Unknown positional option name: {}".format(option_name))
        self.positional_options.extend(option_list)

    def set_driver_mandatory_options(self, **mandatory_option_values):
        for mandatory_option_name, mandatory_option_value in mandatory_option_values.items():
            if mandatory_option_name in self.positional_options:
                self.update_option_container(self.positional_options_and_values, mandatory_option_name, mandatory_option_value)
            else:
                self.update_option_container(self.general_options_and_values, mandatory_option_name, mandatory_option_value)

    def update_option_container(self, container, option_name, option_value):
        if option_value is None:
            container.update({option_name: self.construct_option_default_value(option_name)})
        else:
            container.update({option_name: self.construct_option_value(option_name, option_value)})

    def construct_option_default_value(self, option_name):
        option_default_values = {
            "file_name": str(Path(tc_parameters.WORKING_DIR, "{}_{}.log".format(self.driver_direction, get_unique_id()))),
        }
        return option_default_values[option_name]

    def construct_option_value(self, option_name, option_value):
        path_based_option_values = {
            "file_name": str(Path(tc_parameters.WORKING_DIR, option_value)),
        }
        if option_name in path_based_option_values:
            return path_based_option_values[option_name]
        return option_value

    def get_driver_io_option_values(self):
        driver_io_option_values = self.get_values_for_container(self.driver_io_options)
        return driver_io_option_values[0]

    def get_positional_option_value(self):
        positional_option_values = self.get_values_for_container(self.positional_options)
        return positional_option_values[0] if positional_option_values else None

    def get_values_for_container(self, container):
        found_option_values = []
        for option in container:
            if option in self.general_options_and_values:
                found_option_values.append(self.general_options_and_values[option])
            elif option in self.positional_options_and_values:
                found_option_values.append(self.positional_options_and_values[option])
            else:
                raise ValueError("Can not find value for option: {}".format(option))

        return found_option_values
