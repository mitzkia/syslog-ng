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

import os


class TestCaseParameters(dict):
    def __init__(self, testcase_context):
        testcase_name = testcase_context.node.name.replace("[", "_").replace("]", "_")
        testcase_file = testcase_context.node.fspath
        reports_base_path = testcase_context.getfixturevalue("reports")
        framework_root_dir = os.getcwd()

        self.testcase_parameters = {
            "dir_paths": {
                "working_dir": os.path.join(*[framework_root_dir, reports_base_path, testcase_name]),
                "relative_working_dir": os.path.join(*[reports_base_path, testcase_name]),
            },
            "file_paths": {
                "report_file": os.path.join(*[framework_root_dir, reports_base_path, testcase_name, "testcase_{}.log".format(testcase_name)]),
                "testcase_file": testcase_file,
            },
            "testcase_name": testcase_name,
            "loglevel": testcase_context.getfixturevalue("loglevel")
        }

        super().__init__(self.testcase_parameters)
