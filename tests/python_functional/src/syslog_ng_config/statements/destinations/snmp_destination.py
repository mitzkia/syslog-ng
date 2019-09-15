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
from src.syslog_ng_config.statements.destinations.destination_driver import DestinationDriver
from src.syslog_ng_config.statements.option_handlers.option_handler import OptionHandler


class SnmpBasedOptionHandler(OptionHandler):
    def __init__(self, non_uniq_options):
        self.non_uniq_options = non_uniq_options
        super(SnmpBasedOptionHandler, self).__init__()

    def render_options(self):
        for option_item in self.non_uniq_options:
            for option_name, option_value in option_item.items():
                yield option_name, option_value


class SNMPDestination(DestinationDriver):
    def __init__(self, options):
        self.driver_name = "snmp"
        self.options = options
        self.__snmp_based_option_handler = SnmpBasedOptionHandler(self.options)

        super(SNMPDestination, self).__init__(option_handler=self.__snmp_based_option_handler)
