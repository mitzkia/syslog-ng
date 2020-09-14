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
from src.driver_io.file.file_reader import FileReader
from src.syslog_ng_config.config_statement import ConfigStatement
from src.syslog_ng_config.statements.destinations.destination_driver import DestinationDriver


class FileDestination(DestinationDriver):
    def __init__(self, file_name, **options):
        self.driver_name = "file"
        self.path = Path(tc_parameters.WORKING_DIR, file_name)
        self.options = options
        self.options.update({"file_name": self.path})
        self.config_statement = ConfigStatement
        self.file_reader = FileReader
        super(FileDestination, self).__init__(self.config_statement(self.options, "destination", self.driver_name), self.file_reader(self.path))
