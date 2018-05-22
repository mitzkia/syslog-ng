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

from src.common.random_id import RandomId

class ConfigTree(object):
    def __init__(self, empty_driver_content=None):
        if empty_driver_content:
            self.driver_name = empty_driver_content["driver_name"]
            self.empty_driver_content = empty_driver_content
        self.global_config = None
        self.stmt_id = "stmtid_{}".format(RandomId(use_static_seed=False).get_unique_id())
        self.driver_id = "driverid_{}".format(RandomId(use_static_seed=False).get_unique_id())
        self.root_node_name = None
        self.stmt_node = None
        self.driver_node = None

    def register_statement(self, root_node_name):
        self.global_config[root_node_name].update({self.stmt_id: {}}) ## effective registration
        self.root_node_name = root_node_name ## backup root_node_name
        self.stmt_node = self.global_config[root_node_name][self.stmt_id] ## backup created statement node
        return self.stmt_node

    def unregister_statement(self):
        self.global_config[self.root_node_name].pop(self.stmt_id)

    def register_driver(self, parent_stmt_node=None):
        if parent_stmt_node is None:
            parent_stmt_node = self.stmt_node
        parent_stmt_node.update({self.driver_id: self.empty_driver_content}) ## effective registration
        self.driver_node = parent_stmt_node[self.driver_id] # backup created driver node
        return self.driver_node

    def unregister_driver(self):
        self.stmt_node.pop(self.driver_id)

    def register_options(self, options, parent_driver_node=None):
        if parent_driver_node is None:
            parent_driver_node = self.driver_node['driver_options']
        for option_name, option_value in options.items():
            parent_driver_node.update({option_name: option_value}) ## effective registration

    def unregister_options(self, options):
        for option_name in options:
            self.driver_node['driver_options'].pop(option_name)

    def get_statement(self):
        return self.stmt_node

    def build(self, global_config, root_node_name, options):
        self.global_config = global_config
        self.register_statement(root_node_name)
        self.register_driver()
        self.register_options(options)

    def build_driver_without_parent(self, global_config, options):
        self.global_config = global_config
        driver_node_without_parent = {
            self.driver_id: self.empty_driver_content
        }
        self.register_options(options, parent_driver_node=driver_node_without_parent[self.driver_id]['driver_options'])

    def build_global_options(self, global_config, options):
        self.global_config = global_config
        self.register_options(options, global_config['global_options'])
