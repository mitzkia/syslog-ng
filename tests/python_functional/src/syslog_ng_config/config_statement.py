#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2020 Balabit
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


class ConfigStatement(object):
    def __init__(self, options, group_type, driver_name):
        self.group_type = group_type
        self.driver_name = driver_name
        self.options = options
        self.positional_parameters = []
        if "file_name" in self.options:
            self.positional_parameters = [str(self.options["file_name"])]
            del self.options["file_name"]

    def get_path(self):
        return Path(self.positional_parameters[0])

    def set_path(self, pathname):
        self.positional_parameters = [str(Path(tc_parameters.WORKING_DIR, pathname))]
