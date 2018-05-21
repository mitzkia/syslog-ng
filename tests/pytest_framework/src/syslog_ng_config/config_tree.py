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

from src.common.random import Random

class ConfigTree(object):
    def __init__(self):
        self.statement_id = None
        self.driver_id = None
        self.statement_node = None
        self.driver_node = None

    def register_new_statement(self, root_node, root_node_name):
        self.statement_id = "{}_{}".format(root_node_name, Random(use_static_seed=False).get_unique_id())
        root_node.update({self.statement_id: {}})
        self.statement_node = root_node[self.statement_id]
        return self.statement_node

    def register_new_driver(self, statement_node, driver_name, statement_short_name):
        self.driver_id = "{}_{}".format(driver_name, Random(use_static_seed=False).get_unique_id())
        empty_driver_node = {
            "driver_name": driver_name,
            "mandatory_option_name": [],
            "driver_options": {},
            "statement_short_name": statement_short_name
        }
        statement_node.update({self.driver_id: empty_driver_node})
        self.driver_node = statement_node[self.driver_id]
        return self.driver_node

    def get_mandatory_option_name(self):
        return self.driver_node["mandatory_option_name"]

    def get_mandatory_option_value(self):
        mandatory_option_name = self.get_mandatory_option_name()
        return self.driver_node["driver_options"][mandatory_option_name]
