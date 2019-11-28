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
# from pathlib2 import Path
# import src.testcase_parameters.testcase_parameters as tc_parameters
# from src.common.random_id import get_unique_id


def get_dict_node_recursively(base_dictionary, nodes_to_option, create=False):
    current_dict = base_dictionary
    for node in nodes_to_option:
        if node not in current_dict:
            if create:
                current_dict[node] = {}
            else:
                return False
        current_dict = current_dict[node]
    return current_dict


class StatementOptionHandler(object):
    def __init__(self):
        self.options = None
        self.option_properties = {}

    def init_options(self, options):
        self.options = options

    def set_option_property(self, option_name, is_driverio=False, is_positional=False, formatter=None):
        self.option_properties.update({option_name: {"is_driverio": is_driverio, "is_positional": is_positional, "formatter": formatter}})

    def set_block_option_property(self, path_to_option_in_dict, option_name, is_driverio=False, is_positional=False, formatter=None):
        dict_node_to_option = get_dict_node_recursively(self.option_properties, path_to_option_in_dict, create=True)
        dict_node_to_option.update({option_name: {"is_driverio": is_driverio, "is_positional": is_positional, "formatter": formatter}})

    def get_property_for_option(self, path_to_option_in_dict, option_name, option_property):
        if path_to_option_in_dict is None:
            try:
                return self.option_properties[option_name][option_property]
            except KeyError:
                return False

        dict_node_to_option = get_dict_node_recursively(self.option_properties, path_to_option_in_dict)
        try:
            if dict_node_to_option and option_name in dict_node_to_option:
                return dict_node_to_option[option_name][option_property]
            else:
                return False
        except KeyError:
            raise

    def get_positional_options(self):
        positional_dict = self.get_options_by_criteria(criteria={"is_positional": True})
        # import pdb; pdb.set_trace()
        # assert len(positional_dict.keys()) != 1
        if positional_dict:
            return list(positional_dict.values())[0]
        return None

    def get_driverio_options(self):
        return self.get_options_by_criteria(criteria={"is_driverio": True})

    def get_non_positional_options(self):
        return self.get_options_by_criteria(criteria={"is_positional": False})

    def get_options_by_criteria(self, criteria):
        assert len(criteria.keys()) == 1
        option_type = list(criteria.keys())[0]
        option_type_bool = criteria[option_type]

        formatted_options = {}
        path_to_option_in_dict = []

        if self.options:
            self._get_options_by_criteria_helper(option_type, option_type_bool, self.options, path_to_option_in_dict, formatted_options)

        return formatted_options

    def _get_options_by_criteria_helper(self, option_type, option_type_bool, base_options, path_to_option_in_dict, formatted_options):
        for option_name, option_value in base_options.items():
            if isinstance(option_value, dict):
                new_stack = path_to_option_in_dict.copy()
                new_stack.append(option_name)
                self._get_options_by_criteria_helper(option_type, option_type_bool, option_value, new_stack, formatted_options)
            else:
                if self.get_property_for_option(path_to_option_in_dict, option_name, option_type) == option_type_bool:
                    option_formatter = self.get_property_for_option(path_to_option_in_dict, option_name, "formatter")
                    formatted_option_value = self.run_option_formatter(option_name, option_value, option_formatter)
                    current_node = get_dict_node_recursively(formatted_options, path_to_option_in_dict, create=True)
                    current_node.update({option_name: formatted_option_value})

    def run_option_formatter(self, option_name, option_value, option_formatter):
        assert option_name is not None
        general_formatted_value = self.run_general_formatter(option_value)
        if general_formatted_value is False and option_formatter:
            formatted_value = option_formatter(option_value)
            return formatted_value
        elif general_formatted_value is False and not option_formatter:
            return option_value
        else:
            return general_formatted_value

    def run_general_formatter(self, option_value):
        if option_value == "empty":
            return ""
        elif option_value == "''":
            return option_value
        else:
            return False
