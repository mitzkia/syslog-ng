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


class DriverRegister(ConfigNodeRegister):

    def __init__(self):
        ConfigNodeRegister.__init__(self)
        self.empty_driver_node = {"driver_name": "", "mandatory_option_names": "", "driver_options": {}}

    def register_driver_node(self, root_node, driver_name):
        driver_id = "{}_{}".format(driver_name, Random(use_static_seed=False).get_unique_id())
        self.empty_driver_node["driver_name"] = driver_name
        root_node.update({driver_id: self.empty_driver_node})
        self.save_root_node(root_node)
        self.save_node_id(driver_id)
        self.save_created_node(root_node[driver_id])
        self.save_node_name(driver_name)
        return self.created_node
