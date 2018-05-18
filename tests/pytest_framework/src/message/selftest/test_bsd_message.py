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
from src.message.bsd_formatter import BSDFormatter


def test_default_bsd_message_parts():
    bsd_message = BSDFormatter()
    assert set(list(bsd_message.default_message_parts)) == {'priority', 'bsd_timestamp', 'hostname', 'program', 'pid',
                                                            'message'}


@pytest.mark.parametrize("message_parts, expected_result", [
    (
        {
            "priority": "42", "bsd_timestamp": "Jun  1 08:05:42", "hostname": "testhost", "program": "testprogram",
            "pid": "9999", "message": "test message"
        },
        "<42>Jun  1 08:05:42 testhost testprogram[9999]: test message\n"
    ),
    (
        {"message": "test message\n"},
        "test message\n"
    ),
])
def test_construct_message(message_parts, expected_result):
    bsd_message = BSDFormatter()
    assert bsd_message.construct_message(message_parts) == expected_result
