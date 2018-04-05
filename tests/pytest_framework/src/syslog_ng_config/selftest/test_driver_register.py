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
from src.syslog_ng_config.driver_register import DriverRegister

def test_register_driver_node():
    driver_register = DriverRegister()
    syslog_ng_config = {"sources":{"src_stmt_id_1234": {}}}
    driver_name = "file"
    created_node = driver_register.register_driver_node(root_node=syslog_ng_config["sources"]["src_stmt_id_1234"], driver_name=driver_name)
    assert created_node == {
        'driver_name': driver_name,
        'mandatory_option_names': '',
        'driver_options': {}
    }
    generated_random_id = driver_register.node_id.split("_")[1]
    assert syslog_ng_config == {"sources": {"src_stmt_id_1234": {"{}_{}".format(driver_name, generated_random_id): created_node}}}
