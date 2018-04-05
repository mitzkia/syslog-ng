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

from src.syslog_ng_config.config_node_register import ConfigNodeRegister
from src.common.random import Random


class LogPaths(ConfigNodeRegister):
    def __init__(self):
        ConfigNodeRegister.__init__(self)
        self.syslog_ng_known_statements = ["sources", "destinations", "templates", "filters", "rewrites"]
        self.empty_logpath = {
            "sources": [],
            "destinations": [],
            "templates": [],
            "filters": [],
            "rewrites": [],
            "flags": []
        }


    def register_logpath_node(self, root_node, **kwargs):
        node_name = "logpath"
        node_id = "{}_{}".format(node_name, Random(use_static_seed=False).get_unique_id())
        for statement in self.syslog_ng_known_statements:
            if statement in kwargs:
                self.update_logpath_statement_list(self.empty_logpath[statement], kwargs[statement])
        root_node.update({node_id: self.empty_logpath})
        self.save_created_node(root_node[node_id])
        self.save_node_id(node_id)
        return self.created_node

    def add_sources(self, sources):
        self.update_logpath_statement_list(self.created_node['sources'], sources)

    def add_destinations(self, destinations):
        self.update_logpath_statement_list(self.created_node['destinations'], destinations)

    def add_flags(self, flags):
        self.update_logpath_statement_list(self.created_node['flags'], flags)

    @staticmethod
    def update_logpath_statement_list(logpath_node, statements):
        if isinstance(statements, list):
            for driver in statements:
                logpath_node.append(driver.get_statement_id())
        else:
            logpath_node.append(statements.get_statement_id())
