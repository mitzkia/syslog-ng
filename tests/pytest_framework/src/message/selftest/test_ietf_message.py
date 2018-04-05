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
from src.message.ietf_message import IETFMessage


def test_default_ietf_message_parts():
    ietf_message = IETFMessage()
    assert set(list(ietf_message.default_message_parts)) == {'priority', 'syslog_protocol_version', 'iso_timestamp',
                                                             'hostname', 'program', 'pid', 'message_id', 'sdata',
                                                             'message'}


@pytest.mark.parametrize("message_parts, expected_result", [
    (
        {
            'priority': '165', 'syslog_protocol_version': '1', 'iso_timestamp': '2003-10-11T22:14:15.003Z',
            'hostname': 'mymachine.example.com', 'program': 'evntslog', 'pid': '-', 'message_id': 'ID47',
            'sdata': '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"]',
            'message': 'test message'
        },
        '191 <165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"] \ufefftest message\n'
    ),
])
def test_construct_message(message_parts, expected_result):
    ietf_message = IETFMessage()
    assert ietf_message.construct_message(message_parts) == expected_result
