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

class LogPath(object):
    def __init__(self):
        self.syslog_ng_known_statements = ["sources", "parsers", "destinations", "flags"]
        self.empty_logpath = {
            "sources": [], "parsers": [], "destinations": [], "flags": []
        }
        self.logpath_id = None
        self.logpath_node = None

    def register_new_logpath(self, root_node, **kwargs):
        self.logpath_id = "{}_{}".format("logpath", RandomId(use_static_seed=False).get_unique_id())
        for logpath_element, logpath_element_value  in kwargs.items():
            if logpath_element not in self.syslog_ng_known_statements:
                raise Exception("Unknown logpath element: {}".format(logpath_element))
            else:
                if logpath_element == "flags":
                    self.update_logpath_flags_list(self.empty_logpath[logpath_element], logpath_element_value)
                else:
                    self.update_logpath_statement_list(self.empty_logpath[logpath_element], logpath_element_value)
        self.logpath_node = {self.logpath_id: self.empty_logpath}
        root_node.update(self.logpath_node)
        return self.logpath_node

    def add_sources(self, sources):
        self.update_logpath_statement_list(self.logpath_node["sources"], sources)

    def add_destinations(self, destinations):
        self.update_logpath_statement_list(self.logpath_node["destinations"], destinations)

    def add_flags(self, flags):
        self.update_logpath_statement_list(self.logpath_node["flags"], flags)

    @staticmethod
    def update_logpath_statement_list(logpath_node, statements):
        for statement in statements:
            logpath_node.append(statement.stmt_id)

    @staticmethod
    def update_logpath_flags_list(logpath_node, flags):
        logpath_node.append(flags)
