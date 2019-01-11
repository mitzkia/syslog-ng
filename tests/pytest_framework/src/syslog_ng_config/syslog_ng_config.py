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

from src.driver_io.file.file_io import FileIO
from src.syslog_ng_config.renderer import ConfigRenderer
from src.syslog_ng_config.statements.logpath.logpath import LogPath
from src.syslog_ng_config.statements.sources.file_source import FileSource
from src.syslog_ng_config.statements.destinations.file_destination import FileDestination
from src.syslog_ng_config.statements.destinations.stream_based_network_destinations import StreamBasedNetworkDestinations
from src.syslog_ng_config.statements.sources.stream_based_network_sources import StreamBasedNetworkSources
from src.syslog_ng_config.statement_group import StatementGroup
from src.common.operations import cast_to_list
from src.syslog_ng_config.statements.filters.filter import Filter


class SyslogNgConfig(object):
    def __init__(self, logger_factory, instance_paths, syslog_ng_version):
        self.__instance_paths = instance_paths
        self.__config_path = instance_paths.get_config_path()
        self.__logger_factory = logger_factory
        self.__logger = logger_factory.create_logger("SyslogNgConfig")
        self.__syslog_ng_config = {
            "version": syslog_ng_version,
            "global_options": {},
            "statement_groups": [],
            "logpath_groups": [],
        }

    def write_config_content(self):
        rendered_config = ConfigRenderer(self.__syslog_ng_config, self.__instance_paths).get_rendered_config()
        self.__logger.info(
            "Used config \
        \n->Content:[{}]".format(
                rendered_config
            )
        )
        FileIO(self.__logger_factory, self.__config_path).rewrite(rendered_config)

    @staticmethod
    def __create_statement_group(group_type, statements):
        statement_group = StatementGroup(group_type)
        statement_group.update_group_with_statements(cast_to_list(statements))
        return statement_group

    @staticmethod
    def __create_logpath_group(statements=None, flags=None):
        logpath = LogPath()
        if statements:
            logpath.update_logpath_with_groups(cast_to_list(statements))
        if flags:
            logpath.add_flags(cast_to_list(flags))
        return logpath

    def create_global_options(self, **kwargs):
        self.__syslog_ng_config["global_options"].update(kwargs)

    def create_file_source(self, **kwargs):
        return FileSource(self.__logger_factory, self.__instance_paths, **kwargs)

    def create_network_source(self, **kwargs):
        return StreamBasedNetworkSources("network", self.__logger_factory, self.__instance_paths, **kwargs)

    def create_file_destination(self, **kwargs):
        return FileDestination(self.__logger_factory, self.__instance_paths, **kwargs)

    def create_network_destination(self, **kwargs):
        return StreamBasedNetworkDestinations("network", self.__logger_factory, self.__instance_paths, **kwargs)

    def create_syslog_destination(self, **kwargs):
        return StreamBasedNetworkDestinations("syslog", self.__logger_factory, self.__instance_paths, **kwargs)

    def create_filter(self, **kwargs):
        return Filter(self.__logger_factory, **kwargs)

    def create_source_group(self, drivers):
        source_group = self.__create_statement_group("source", drivers)
        self.__syslog_ng_config["statement_groups"].append(source_group)
        return source_group

    def create_destination_group(self, drivers):
        destination_group = self.__create_statement_group("destination", drivers)
        self.__syslog_ng_config["statement_groups"].append(destination_group)
        return destination_group

    def create_filter_group(self, filters):
        filter_group = self.__create_statement_group("filter", filters)
        self.__syslog_ng_config["statement_groups"].append(filter_group)
        return filter_group

    def create_logpath(self, statements=None, flags=None):
        logpath = self.__create_logpath_group(statements, flags)
        self.__syslog_ng_config["logpath_groups"].append(logpath)
        return logpath

    def create_inner_logpath(self, statements=None, flags=None):
        inner_logpath = self.__create_logpath_group(statements, flags)
        return inner_logpath
