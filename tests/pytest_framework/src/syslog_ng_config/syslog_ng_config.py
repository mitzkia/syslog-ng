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
from src.syslog_ng_config.driver_register import DriverRegister
from src.syslog_ng_config.option_setter import OptionSetter
from src.syslog_ng_config.drivers.file_based_driver import FileBasedDriver
from src.syslog_ng_config.logpath import LogPaths
from src.syslog_ng_config.renderer import ConfigRenderer
from src.driver_io.file_based.file_interface import FileInterface


class SyslogNgConfig(object):
    def __init__(self, logger_factory, file_register, instance_parameters, syslog_ng_version):
        self.logger_factory = logger_factory
        self.file_register = file_register
        self.instance_parameters = instance_parameters
        self.config_path = instance_parameters['file_paths']['config_path']
        self.fileinterface = FileInterface(logger_factory)
        self.syslog_ng_version = syslog_ng_version

        self.syslog_ng_config = {
            "version": self.syslog_ng_version,
            "include": ["scl.conf"],
            "module": [],
            "define": {},
            "channel": [],
            "block": [],
            "global_options": {},
            "sources": {},
            "filters": {},
            "parsers": {},
            "templates": {},
            "rewrites": {},
            "destinations": {},
            "logpaths": {},
        }
        self.raw_config = None

    @staticmethod
    def init_driver_registration():
        statement = ConfigNodeRegister()
        driver = DriverRegister()
        option_setter = OptionSetter()
        return statement, driver, option_setter

    def driver_init(self, statement_type, driver_name, baseclass):
        statement, driver, option_setter = self.init_driver_registration()
        root_node = "{}s".format(statement_type)
        statement_node = statement.register_empty_node(self.syslog_ng_config[root_node], statement_type)
        driver_node = driver.register_driver_node(statement_node, driver_name)
        driver_object = baseclass(statement, driver, option_setter, self.logger_factory, self.instance_parameters)
        return driver_object, driver_node

    def write_config_content(self):
        if self.raw_config:
            rendered_config = self.raw_config
        else:
            rendered_config = ConfigRenderer(self.syslog_ng_config).syslog_ng_config_content
        self.fileinterface.write_content(self.config_path, rendered_config, open_mode='w')

    def set_raw_config(self, raw_config):
        self.raw_config = raw_config

    def add_global_options(self, options):
        option_setter = OptionSetter()
        option_setter.add_options(self.syslog_ng_config['global_options'], options)

    def get_file_source(self, options=None):
        driver_object, driver_node = self.driver_init("source", "file", FileBasedDriver)
        driver_object.add_options(driver_node, options)
        return driver_object

    def get_file_destination(self, options=None):
        driver_object, driver_node = self.driver_init("destination", "file", FileBasedDriver)
        driver_object.add_options(driver_node, options)
        return driver_object

    def create_logpath(self, **kwargs):
        logpath = LogPaths()
        logpath.register_logpath_node(self.syslog_ng_config['logpaths'], **kwargs)
        return logpath
