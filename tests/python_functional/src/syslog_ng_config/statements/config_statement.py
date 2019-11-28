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


class ConfigStatement(object):
    def __init__(self, option_handler):
        self.__option_handler = option_handler

    def reload_option_handler(self):
        self.__option_handler.reload_options(self.options)

    def render_driver_options(self):
        rendered_driver_config = ""
        rendered_driver_config += self.render_positional_options()
        rendered_driver_config += self.render_options()
        return rendered_driver_config

    def render_positional_options(self):
        rendered_positional_options = ""
        for positional_option_value in self.__option_handler.get_positional_option_values():
            if positional_option_value is None:
                rendered_positional_options += "\n"
            else:
                rendered_positional_options += "    {}\n".format(positional_option_value)
        return rendered_positional_options

    def render_options(self):
        rendered_options = ""
        indentation = " " * 4
        for option_name, option_value in self.__option_handler.options.items():
            if option_value is None:
                rendered_options += "{}{}()\n".format(indentation, option_name)
            elif option_name is None:
                rendered_options += "{}{}\n".format(indentation, option_value)
            elif option_name and option_value:
                rendered_options += "{}{}({})\n".format(indentation, option_name, option_value)
            else:
                raise ValueError
        return rendered_options

    # def get_rendered_driver(self):
    #     rendered_driver = ""
    #     if self.__option_handler.get_positional_option():
    #         rendered_driver += "    {}\n".format(self.__option_handler.get_positional_option())

    #     option_indentation_level = 1
    #     for option_name, option_value in self.__option_handler.render_options():
    #         if isinstance(option_value, dict):
    #             rendered_driver += self.render_option_block(option_name, option_value, option_indentation_level)
    #         else:
    #             rendered_driver += self.render_option(option_name, option_value, option_indentation_level)

    #     return rendered_driver

    # def render_option(self, option_name, option_value, option_indentation_level):
    #     indentation = " " * 4
    #     if option_value is None:
    #         return "{}{}()\n".format(indentation * option_indentation_level, option_name)
    #     if not option_name:
    #         return "{}{}\n".format(indentation * option_indentation_level, option_value)
    #     return "{}{}({})\n".format(indentation * option_indentation_level, option_name, option_value)

    # def render_option_block(self, option_name, option_value, option_indentation_level):
    #     indentation = " " * 4
    #     inner_rendered_block = ""
    #     inner_rendered_block += "{}{}(\n".format(indentation * option_indentation_level, option_name)
    #     for inner_block_name, inner_block_value in option_value.items():
    #         if isinstance(inner_block_value, dict):
    #             option_indentation_level += 1
    #             inner_rendered_block += self.render_option_block(inner_block_name, inner_block_value, option_indentation_level)
    #         else:
    #             inner_rendered_block += self.render_option(inner_block_name, inner_block_value, option_indentation_level)
    #     inner_rendered_block += "{})\n".format(indentation * option_indentation_level)
    #     return inner_rendered_block
