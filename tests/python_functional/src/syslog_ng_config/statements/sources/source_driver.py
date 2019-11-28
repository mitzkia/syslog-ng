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
from src.syslog_ng_config.statements.config_statement import ConfigStatement
from src.syslog_ng_config.statements.sources.source_writer import SourceWriter


class SourceDriver(ConfigStatement):
    def __init__(self, option_handler, driver_io_cls=None):
        self.group_type = "source"
        self.group_direction = "input"

        self.option_handler = option_handler
        self.driver_io_cls = driver_io_cls

        self.source_writer = None
        self.init_source_writer()

        super(SourceDriver, self).__init__(self.option_handler)

    def init_source_writer(self):
        if self.driver_io_cls and self.option_handler.get_driverio_options():
            self.source_writer = SourceWriter(self.driver_io_cls)
            self.source_writer.init_driver_io(self.option_handler.get_driverio_options())

    def write_log(self, formatted_log, counter=1):
        if self.source_writer:
            self.source_writer.write_log(formatted_log, counter=counter)
        else:
            raise ValueError("SourceWriter was not defined")
