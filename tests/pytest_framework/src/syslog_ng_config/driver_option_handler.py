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
from src.syslog_ng_config.option_setter import OptionSetter
from src.common.random import Random

class DriverOptionHandler(object):
    def __init__(self, config_tree):
        self.config_tree = config_tree
        self.option_setter = OptionSetter()
        self.mandatory_option_value = None

    def add_options(self, options):
        self.option_setter.add_options(self.config_tree.driver_node['driver_options'], options)

    def remove_options(self, options):
        self.option_setter.remove_options(options)

    def set_file_path_mandatory_option(self, options, file_path_prefix, working_dir):
        random_id = Random(use_static_seed=False).get_unique_id()

        mandatory_option_name = "file_path"
        if not mandatory_option_name in options.keys():
            self.mandatory_option_value = os.path.join(working_dir, "{}_{}.log".format(file_path_prefix, random_id))
            mandatory_option = {mandatory_option_name: self.mandatory_option_value}
            options.update(mandatory_option)
        else:
            option_value = options[mandatory_option_name]
            self.mandatory_option_value = os.path.join(working_dir, "{}_{}.log".format(file_path_prefix, option_value))
            options.update({mandatory_option_name: self.mandatory_option_value})

        self.config_tree.driver_node['mandatory_option_name'] = mandatory_option_name

    def update_file_path_mandatory_option(self, options, file_path_prefix, working_dir):
        mandatory_option_name = "file_path"
        if mandatory_option_name in options.keys():
            option_value = options[mandatory_option_name]
            self.mandatory_option_value = os.path.join(working_dir, "{}_{}.log".format(file_path_prefix, option_value))
            options.update({mandatory_option_name: self.mandatory_option_value})

        self.config_tree.driver_node['mandatory_option_name'] = mandatory_option_name
