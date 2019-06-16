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
from pathlib2 import Path

import src.testcase_parameters.testcase_parameters as tc_parameters
from src.common.random_id import get_unique_id
from src.driver_io.file.file_io import FileIO
from src.syslog_ng_config.statements.sources.source_writer import SourceWriter


class FileSource(object):
    def __init__(self, file_name, **options):
        self.driver_name = "file"
        self.group_type = "source"
        self.options = options
        self.calculate_positional_option(file_name)
        self.source_writer = SourceWriter(FileIO)

    def calculate_positional_option(self, file_name):
        if file_name == "":
            self.positional_option = "''"
        elif file_name is None:
            self.positional_option = Path(tc_parameters.WORKING_DIR, "input_fs_{}.log".format(get_unique_id()))
        elif file_name == "skip":
            pass
        else:
            self.positional_option = Path(tc_parameters.WORKING_DIR, file_name)

    def get_path(self):
        return self.positional_option

    def set_path(self, pathname):
        self.positional_option = Path(tc_parameters.WORKING_DIR, pathname)
        self.source_writer.construct_driver_io(self.positional_option)

    def write_log(self, formatted_log, counter=1):
        self.source_writer.write_log(self.get_path(), formatted_log, counter=counter)
