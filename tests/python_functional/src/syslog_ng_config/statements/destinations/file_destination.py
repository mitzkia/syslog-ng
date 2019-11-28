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
from src.message_reader.single_line_parser import SingleLineParser
from src.syslog_ng_config.statements.destinations.destination_driver import DestinationDriver
from src.syslog_ng_config.statements.option_formatters import file_path_formatter
from src.syslog_ng_config.statements.statement_option_handler import StatementOptionHandler


class FileDestination(DestinationDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "file"
        self.options = options
        self.options["file_name"] = file_name

        self.option_handler = StatementOptionHandler()
        self.option_handler.init_options(self.options)
        self.option_handler.set_option_property("file_name", is_driverio=True, is_positional=True, formatter=file_path_formatter)

        super(FileDestination, self).__init__(option_handler=self.option_handler, driver_io_cls=FileIO, line_parser_cls=SingleLineParser)

    # def set_path(self, new_file_name):
    #     self.option_handler.set_driver_mandatory_options(direction="output", file_name=new_file_name)
    #     self.init_destination_reader()

    # def get_path(self):
    #     return self.option_handler.get_positional_option_values()[0]
