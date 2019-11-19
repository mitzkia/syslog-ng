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


class StatementOptionHandler:
    def __init__(self, options):
        self.options = options

        self.mandatory_options = []
        self.driver_io_options = []
        self.positional_options = []

        self.positional_options_and_values = {}

    def reload_options(self, options):
        self.options = options

    def register_option_list(self, option_list, mandatory=True, driver_io=True, positional=True):
        if mandatory:
            self.mandatory_options = option_list
        if driver_io:
            self.driver_io_options = option_list
        if positional:
            self.positional_options = option_list

    def register_mandatory_options(self, option_list):
        self.mandatory_options = option_list

    def register_driver_io_options(self, option_list):
        self.driver_io_options = option_list

    def register_positional_options(self, option_list):
        self.positional_options = option_list

    def get_driver_io_option_values(self):
        driver_io_option_values = []
        for option in self.driver_io_options:
            if option in self.options:
                driver_io_option_values.append(self.options[option])
            elif option in self.positional_options_and_values:
                driver_io_option_values.append(self.positional_options_and_values[option])

        if len(driver_io_option_values) == 1:
            return driver_io_option_values[0]
        return driver_io_option_values

    def get_positional_option_values(self):
        positional_option_values = []
        for option_name, option_value in self.positional_options_and_values.items():
            if isinstance(option_value, Path):
                option_value = str(option_value)
            positional_option_values.append(option_value)

        return positional_option_values

    def construct_option_default_value(self, option_name, direction):
        option_default_values = {
            "ip": "127.0.0.1",
            "port": "1",
            "file_name": str(Path(tc_parameters.WORKING_DIR, "{}_{}.log".format(direction, get_unique_id())))
        }
        return option_default_values[option_name]

    def construct_option_value(self, option_name, option_value, direction):
        if option_value == "skip":
            return None
        if option_value in ["''", '""']:
            return option_value
        if option_name in ["file_name"]:
            return str(Path(tc_parameters.WORKING_DIR, option_value))
        return option_value

    def set_driver_mandatory_options(self, direction=None, **mandatory_option_values):
        # import pdb; pdb.set_trace()
        for mandatory_option_name, mandatory_option_value in mandatory_option_values.items():
            if mandatory_option_name in self.positional_options:
                if mandatory_option_value is None:
                    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYY")
                    self.positional_options_and_values.update({mandatory_option_name: self.construct_option_default_value(mandatory_option_name, direction)})
                else:
                    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
                    self.positional_options_and_values.update({mandatory_option_name: self.construct_option_value(mandatory_option_name, mandatory_option_value, direction)})
                continue
            if mandatory_option_value is None:
                print("PPPPPPPPPPPPPPPPPPPPPPPPP")
                self.options.update({mandatory_option_name: self.construct_option_default_value(mandatory_option_name, direction)})
            else:
                print("WWWWWWWWWWWWWWWWWWWWWWWWW")
                self.options.update({mandatory_option_name: self.construct_option_value(mandatory_option_name, mandatory_option_value, direction)})
