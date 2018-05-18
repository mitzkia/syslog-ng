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


def test_register_empty_node():
    config_node_register = ConfigNodeRegister()
    syslog_ng_config = {"sources": {}}
    created_node = config_node_register.register_empty_node(root_node=syslog_ng_config["sources"], node_name="src")
    generated_random_id = config_node_register.node_id.split("_")[1]
    assert syslog_ng_config == {"sources": {"src_{}".format(generated_random_id): {}}}
    assert created_node == {}


def test_delete_node():
    config_node_register = ConfigNodeRegister()
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {}}}
    config_node_register.root_node = syslog_ng_config["sources"]
    config_node_register.created_node = syslog_ng_config
    config_node_register.node_id = "src_stmt_id_1234"
    config_node_register.delete_node()
    assert config_node_register.created_node == {"sources": {}}
