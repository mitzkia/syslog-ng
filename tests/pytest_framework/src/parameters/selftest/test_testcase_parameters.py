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

from src.parameters.test_case import TestCaseParameters


def test_testcase_parameters(request):
    tcp = TestCaseParameters(request)
    assert set(list(tcp.testcase_parameters)) == {"testcase_name", "dir_paths", "file_paths", "loglevel"}
    assert set(list(tcp.testcase_parameters["dir_paths"])) == {"working_dir", "relative_working_dir"}
    assert set(list(tcp.testcase_parameters["file_paths"])) == {"report_file", "testcase_file"}
