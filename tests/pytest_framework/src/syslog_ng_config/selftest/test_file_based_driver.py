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

import re
from src.syslog_ng_config.drivers.file_based_driver import FileBasedDriver
from src.syslog_ng_config.config_node_register import ConfigNodeRegister
from src.syslog_ng_config.driver_register import DriverRegister
from src.syslog_ng_config.option_setter import OptionSetter


def get_dependencies(tc_unittest):
    statement = ConfigNodeRegister()
    driver = DriverRegister()
    driver.created_node = {"mandatory_option_name": "file_path"}
    driver.node_name = "file"
    option_setter = OptionSetter()
    file_based_driver = FileBasedDriver(statement, driver, option_setter, tc_unittest.fake_logger_factory(), tc_unittest.fake_syslog_ng_instance_parameters())
    return file_based_driver

def test_add_options_prefix_used(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    options = {"file_path": "input"}
    file_based_driver.add_options(driver_node=driver_node, options=options)
    assert re.findall("input_file_[0-9]{5}.log", driver_node['driver_options']['file_path']) is not []
    assert len(driver_node['driver_options']) == 1

def test_add_options_prefix_and_options_used(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    options = {"file_path": "input", "option_name": "option_value"}
    file_based_driver.add_options(driver_node=driver_node, options=options)
    assert re.findall("input_file_[0-9]{5}.log", driver_node['driver_options']['file_path']) is not []
    assert driver_node['driver_options']['option_name'] == "option_value"
    assert len(driver_node['driver_options']) == 2

def test_add_options_options_used(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    options = {"option_name": "option_value"}
    file_based_driver.add_options(driver_node=driver_node, options=options)
    assert re.findall("file_[0-9]{5}\.log", driver_node['driver_options']['file_path']) is not []
    assert driver_node['driver_options']['option_name'] == "option_value"
    assert len(driver_node['driver_options']) == 2

def test_add_options_prefix_generated(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    file_based_driver.add_options(driver_node=driver_node, options=None)
    assert re.findall("file_[0-9]{5}.log", driver_node['driver_options']['file_path']) is not []
    assert len(driver_node['driver_options']) == 1

def test_update_options_only_prefix(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    file_based_driver.add_options(driver_node=driver_node, options=None)
    options = {"file_path": "input"}
    file_based_driver.update_options(options=options)
    assert re.findall("input_file_[0-9]{5}.log", driver_node['driver_options']['file_path']) is not []
    assert len(driver_node['driver_options']) == 1

def test_update_options_prefix_and_options(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    file_based_driver.add_options(driver_node=driver_node, options=None)
    options = {"file_path": "input", "option_name": "option_value"}
    file_based_driver.update_options(options=options)
    assert re.findall("input_file_[0-9]{5}.log", driver_node['driver_options']['file_path']) is not []
    assert driver_node['driver_options']['option_name'] == "option_value"
    assert len(driver_node['driver_options']) == 2

def test_remove_options(tc_unittest):
    file_based_driver = get_dependencies(tc_unittest)
    syslog_ng_config = {"sources": {"src_stmt_id_1234": {"driver_id_1234": {"driver_options": {}}}}}
    driver_node = syslog_ng_config["sources"]["src_stmt_id_1234"]["driver_id_1234"]
    options = {"file_path": "input", "option_name": "option_value"}
    file_based_driver.add_options(driver_node=driver_node, options=options)
    file_based_driver.remove_options(options=["file_path", "option_name"])
    assert driver_node['driver_options'] == {}
