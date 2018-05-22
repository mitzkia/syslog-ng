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

import copy
from src.driver_io.file.file_io import FileIO
from src.syslog_ng_config.config_tree import ConfigTree
from src.syslog_ng_config.renderer import ConfigRenderer
from src.syslog_ng_config.statements.logpath.logpath import LogPath
from src.syslog_ng_config.statements.sources.file_source import FileSource
from src.syslog_ng_config.statements.sources.pipe_source import PipeSource
from src.syslog_ng_config.statements.destinations.pipe_destination import PipeDestination
from src.syslog_ng_config.statements.destinations.file_destination import FileDestination
from src.syslog_ng_config.statements.parsers.syslog_parser import SyslogParser

class SyslogNgConfig(object):
    def __init__(self, logger_factory, instance_parameters, syslog_ng_version):
        self.instance_parameters = instance_parameters
        self.config_path = instance_parameters.get_config_path()
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SyslogNgConfig")
        self.raw_config = None
        self.registered_destinations = []
        self.syslog_ng_config = {
            "version": syslog_ng_version,
            "include": ["scl.conf"],
            "global_options": {},
            "sources": {},
            "parsers": {},
            "destinations": {},
            "logpaths": {},
        }

    def write_config_content(self):
        if self.raw_config:
            rendered_config = self.raw_config
        else:
            rendered_config = ConfigRenderer(self.syslog_ng_config).syslog_ng_config_content
        self.logger.info("Used config \
        \n->Content:[{}]".format(rendered_config))
        FileIO(self.logger_factory, self.config_path).rewrite(rendered_config)

    def set_raw_config(self, raw_config):
        self.raw_config = raw_config

    def create_logpath(self, **kwargs):
        logpath = LogPath()
        logpath.register_new_logpath(self.syslog_ng_config["logpaths"], **kwargs)
        return logpath

    def add_global_options(self, options):
        return ConfigTree().build_global_options(self.syslog_ng_config, options)

    def get_file_source(self, options=None, build=True):
        return FileSource(self.syslog_ng_config, self.logger_factory, self.instance_parameters, build, options)

    def get_file_destination(self, options=None, build=True):
        file_destination = FileDestination(self.syslog_ng_config, self.logger_factory, self.instance_parameters, build, options)
        self.registered_destinations.append(file_destination)
        return file_destination

    def get_pipe_source(self, options=None, build=True):
        return PipeSource(self.syslog_ng_config, self.logger_factory, self.instance_parameters, build, options)

    def get_pipe_destination(self, options=None, build=True):
        pipe_destination = PipeDestination(self.syslog_ng_config, self.logger_factory, self.instance_parameters, build, options)
        self.registered_destinations.append(pipe_destination)
        return pipe_destination

    def get_syslog_parser(self, options=None, build=True):
        return SyslogParser(self.syslog_ng_config, self.logger_factory, self.instance_parameters, build, options)

    def read_all_destinations(self):
        output_messages = {}
        for destination in self.registered_destinations:
            output_messages[destination.driver_name] = destination.read_all_messages()
        return output_messages

    def get_all_counters(self):
        counters = {}
        for destination in self.registered_destinations:
            counters[destination.driver_name] = destination.get_counters()
        return counters

    def get_all_destinations(self, options=None, build=True):
        configured_destinations = []
        for class_attribute in dir(self):
            if class_attribute.endswith("destination"):
                original_options = copy.deepcopy(options)
                destination = getattr(self, class_attribute)(options=original_options, build=build)
                configured_destinations.append(destination)
        return configured_destinations
