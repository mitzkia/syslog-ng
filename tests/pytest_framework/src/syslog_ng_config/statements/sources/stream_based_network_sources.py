#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2019 Balabit
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

from src.driver_io.network.socket_stream_io import SocketStreamIO
from src.syslog_ng_config.statements.sources.source_driver import SourceDriver


class StreamBasedNetworkSources(SourceDriver):
    def __init__(self, logger_factory, instance_paths, driver_name, **kwargs):
        super(StreamBasedNetworkSources, self).__init__(logger_factory, SocketStreamIO)
        self.__options = kwargs
        self.__driver_name = driver_name
        self.__positional_option = "ip"

    @property
    def driver_name(self):
        return self.__driver_name

    @property
    def positional_option_name(self):
        return self.__positional_option

    @property
    def options(self):
        return self.__options

    def get_ip(self):
        return self.__options["ip"]

    def get_port(self):
        return self.__options["port"]

    def get_socket(self):
        return (self.get_ip(), self.get_port())

    def write_log(self, formatted_log, counter=1):
        self.sd_write_log(self.get_socket(), formatted_log, counter=counter)
