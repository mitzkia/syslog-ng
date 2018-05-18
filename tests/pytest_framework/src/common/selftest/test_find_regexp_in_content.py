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

import pytest
from src.common.find_in_content import find_regexp_in_content


@pytest.mark.parametrize(
    "regexp, content, expected_counter, expected_result",
    [
        ("^test message$", "test message", 1, True),  # positive
        ("^test message$", "test messageAAA", 1, False),  # negative
        ("^test message$", "test message\ntest message\n", 2, True),  # find double occurrence
        ("test message", "bbb test message aaa", 1, False),  # non regexp will not match
    ],
)
def test_find_regexp_in_content(regexp, content, expected_counter, expected_result):
    assert find_regexp_in_content(regexp, content, expected_counter) == expected_result
