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

from src.syslog_ng_config.config_tree import ConfigTree
from src.syslog_ng_config.file_source_driver import FileSourceDriver
from src.syslog_ng_config.file_destination_driver import FileDestinationDriver
from src.syslog_ng_config.renderer import ConfigRenderer
from src.driver_io.file_based.file_interface import FileInterface
from src.syslog_ng_config.option_setter import OptionSetter
from src.syslog_ng_config.logpath import LogPaths

class SyslogNgConfig(object):
    def __init__(self, logger_factory, instance_parameters, syslog_ng_version):
        self.instance_parameters = instance_parameters
        self.config_path = instance_parameters["file_paths"]["config_path"]
        self.logger_factory = logger_factory
        self.fileinterface = FileInterface(logger_factory)
        self.syslog_ng_version = syslog_ng_version
        self.raw_config = None
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

    def __init_driver_registration(self, root_node_name, driver_name, statement_short_name):
        config_tree = ConfigTree()
        statement_node = config_tree.register_new_statement(root_node=self.syslog_ng_config[root_node_name], root_node_name=root_node_name)
        config_tree.register_new_driver(statement_node=statement_node, driver_name=driver_name, statement_short_name=statement_short_name)
        return config_tree

    def get_file_source(self, options=None):
        config_tree = self.__init_driver_registration(root_node_name="sources", driver_name="file", statement_short_name="src")
        file_source_driver = FileSourceDriver(self.logger_factory, self.instance_parameters, config_tree)
        file_source_driver.configure_options(options)
        return file_source_driver

    def get_file_destination(self, options=None):
        config_tree = self.__init_driver_registration(root_node_name="destinations", driver_name="file", statement_short_name="dst")
        file_destination_driver = FileDestinationDriver(self.logger_factory, self.instance_parameters, config_tree)
        file_destination_driver.configure_options(options)
        return file_destination_driver

    def write_config_content(self):
        if self.raw_config:
            rendered_config = self.raw_config
        else:
            rendered_config = ConfigRenderer(self.syslog_ng_config).syslog_ng_config_content
        self.fileinterface.write_content(self.config_path, rendered_config, open_mode="w")

    def set_raw_config(self, raw_config):
        self.raw_config = raw_config

    def add_global_options(self, options):
        option_setter = OptionSetter()
        option_setter.add_options(self.syslog_ng_config["global_options"], options)

    def create_logpath(self, **kwargs):
        logpath = LogPaths()
        logpath.register_new_logpath(self.syslog_ng_config["logpaths"], **kwargs)
        return logpath
