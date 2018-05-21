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

from src.syslog_ng_config.driver import Driver
from src.syslog_ng_config.driver_io_handler import DriverIOHandler

class DestinationDriver(Driver):
    def __init__(self, logger_factory, instance_parameters, config_tree, driver_io):
        self.config_tree = config_tree
        super().__init__(logger_factory, instance_parameters, config_tree)
        self.driver_io_handler = DriverIOHandler(driver_io)

    def read_msg(self):
        mandatory_option_value = self.config_tree.get_mandatory_option_value()
        self.driver_io_handler.read_msg(mandatory_option_value)

    def read_msgs(self, message_counter):
        mandatory_option_value = self.config_tree.get_mandatory_option_value()
        self.driver_io_handler.read_msgs(mandatory_option_value, message_counter)

    def read_all_msgs(self):
        mandatory_option_value = self.config_tree.get_mandatory_option_value()
        self.driver_io_handler.read_all_msgs(mandatory_option_value)
