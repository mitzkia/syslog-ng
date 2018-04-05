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

from src.syslog_ng_config.drivers.driver_interface import DriverBase
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl

class NetworkBasedDrivers(DriverBase):
    def __init__(self, statement, driver, option_setter, logger_factory, instance_parameters):
        self.syslog_ng_ctl = SyslogNgCtl(logger_factory, instance_parameters)
        DriverBase.__init__(self, statement, driver, option_setter)
        if self.driver.node_name == "default_network_drivers":
            self.driver.created_node['mandatory_option_names'] = ["udp_port", "tcp_port", "rfc5424_tls_port", "rfc5424_tcp_port"]
        else:
            print("Unknown driver: %s" % self.driver.node_name)

    # Options, this part is uses NetworkBasedDriver specific variables, can not put into DriverBase
    def add_options(self, driver_node, options=None):
        if not options:
            options = {}
        options.update(self.set_mandatory_options(options))
        self.option_setter.add_options(driver_node['driver_options'], options)

    def set_mandatory_options(self, options):
        mandatory_options = {}
        for mandatory_option_name in self.driver.created_node['mandatory_option_names']:
            if mandatory_option_name == "udp_port":
                option_value = 4444
            elif mandatory_option_name == "tcp_port":
                option_value = 5555
            elif mandatory_option_name == "rfc5424_tls_port":
                option_value = 6666
            elif mandatory_option_name == "rfc5424_tcp_port":
                option_value = 7777
            else:
                raise SystemExit(1)
            mandatory_options.update({mandatory_option_name: option_value})
        # self.mandatory_option_value = option_value
        return mandatory_options

    def update_options(self, options):
        if self.is_mandatory_option_exist(options):
            options.update(self.set_mandatory_options(options))
        self.option_setter.add_options(self.option_setter.root_node, options)

    def remove_options(self, options):
        self.option_setter.remove_options(options)

    def is_mandatory_option_exist(self, options):
        return len(set(options).intersection(self.driver.created_node['mandatory_option_names'])) != 0
