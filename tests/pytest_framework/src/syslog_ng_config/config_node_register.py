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


class ConfigNodeRegister(object):

    def __init__(self):
        self.root_node = None
        self.created_node = None
        self.node_id = None
        self.node_name = None
        self.node_short_name = None

    def register_empty_node(self, root_node, node_name):
        node_id = "{}_{}".format(node_name, Random(use_static_seed=False).get_unique_id())
        root_node.update({node_id: {}})
        self.save_root_node(root_node)
        self.save_node_id(node_id)
        self.save_created_node(root_node[node_id])
        self.save_node_name(node_name)
        return self.created_node

    def delete_node(self):
        self.root_node.pop(self.node_id)

    def save_root_node(self, root_node):
        self.root_node = root_node

    def save_created_node(self, created_node):
        self.created_node = created_node

    def save_node_id(self, node_id):
        self.node_id = node_id

    def save_node_name(self, node_name):
        if node_name == "source":
            self.node_short_name = "src"
        elif node_name == "destination":
            self.node_short_name = "dst"
        self.node_name = node_name
