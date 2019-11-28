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
from src.syslog_ng_config.statements.sources.source_driver import SourceDriver
from src.syslog_ng_config.statements.statement_option_handler import StatementOptionHandler


class FileSource(SourceDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "file"
        self.options = options

        self.option_handler = StatementOptionHandler(self.options)
        self.option_handler.register_option_list(["file_name"])

        self.option_handler.set_driver_mandatory_options(direction="input", file_name=file_name)

        super(FileSource, self).__init__(option_handler=self.option_handler, driver_io_cls=FileIO)

    def set_path(self, new_file_name):
        self.option_handler.set_driver_mandatory_options(direction="input", file_name=new_file_name)
        self.init_source_writer()

    def get_path(self):
        return self.option_handler.get_positional_option_values()[0]
