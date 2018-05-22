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

from pathlib2 import PosixPath
from src.meta.testcase_meta import TestcaseMeta

def test_testcase_meta(request):
    testcase_meta = TestcaseMeta(request).testcase_meta
    assert set(list(testcase_meta)) == {'testcase_name', 'dirs', 'file_paths', 'loglevel'}
    assert set(list(testcase_meta['dirs'])) == {'working_dir', 'relative_working_dir'}
    assert set(list(testcase_meta['file_paths'])) == {'report_file', 'testcase_file'}

def test_testcase_meta_parent_class_of_paths(request):
    testcase_meta = TestcaseMeta(request).testcase_meta
    for __key, value in testcase_meta["dirs"].items():
        assert isinstance(value, PosixPath) is True

    for __key, value in testcase_meta["file_paths"].items():
        assert isinstance(value, PosixPath) is True
