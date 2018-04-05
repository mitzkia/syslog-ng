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

import re
import socket
import pytest
from src.message.interface import MessageInterface


@pytest.mark.parametrize("message_parts, default_message_parts, expected_result", [
    ({"priority": "38"}, {"priority": "38"}, None),
])
def test_validate_message_parts(tc_unittest, message_parts, default_message_parts, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.validate_message_parts(message_parts, default_message_parts) is expected_result


@pytest.mark.parametrize("message_parts, default_message_parts, expected_result", [
    (
        {"priority": "42"},  # came from user
        {"priority": "38"},  # default value
        {"priority": "42"}),  # user value overwrites default value
    (
        {"priority": "skip"},  # came from user
        {"priority": "38"},  # default value
        {}),  # skip the message part
    (
        {"hostname": "testhostname"},  # came from user
        {"priority": "38", "hostname": "otherhostname"},  # default values
        {'hostname': 'testhostname', 'priority': '38'}),  # using default value, and overwriting default value
])
def test_set_message_parts(tc_unittest, message_parts, default_message_parts, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.set_message_parts(message_parts, default_message_parts) == expected_result


@pytest.mark.parametrize("message_parts, message_counter, expected_result", [
    (
        {},  # use all default values
        1,  # create 1 message
        "<38>Jun  1 08:05:04 {} testprogram[9999]: test message - árvíztűrő tükörfúrógép\n".format(
            socket.gethostname())
    ),
    (
        {},  # use all default values
        2,  # create 2 messages
        "<38>Jun  1 08:05:04 {} testprogram[9999]: test message - árvíztűrő tükörfúrógép\n\
<38>Jun  1 08:05:04 {} testprogram[9999]: test message - árvíztűrő tükörfúrógép\n".format(
            socket.gethostname(), socket.gethostname()
        ),
    ),
    (
        {
            "priority": "42", "bsd_timestamp": "Dec  1 09:06:32", "hostname": "randomhost", "program": "randomprogram",
            "pid": "9999", "message": "test message"
        },  # overwrite very values
        2,  # create 2 messages
        "<42>Dec  1 09:06:32 randomhost randomprogram[9999]: test message\n\
<42>Dec  1 09:06:32 randomhost randomprogram[9999]: test message\n"
    ),
    (
        {
            "priority": "skip", "bsd_timestamp": "skip", "hostname": "skip", "program": "skip", "pid": "skip",
            "message": "test message"
        },  # skipping some message parts
        1,  # create 1 message
        "test message\n"
    ),
    (
        {"bsd_timestamp": "regexp"},  # use default message parts and regexp for bsd_timestamp
        2,  # create 2 messages
        [
            re.compile(
                '<38>[a-zA-Z]{3} ([0-9]{2}| [0-9]{1}) [0-9]{2}:[0-9]{2}:[0-9]{2} %s testprogram[9999]: test message - árvíztűrő tükörfúrógép\n' % socket.gethostname()),
            re.compile(
                '<38>[a-zA-Z]{3} ([0-9]{2}| [0-9]{1}) [0-9]{2}:[0-9]{2}:[0-9]{2} %s testprogram[9999]: test message - árvíztűrő tükörfúrógép\n' % socket.gethostname())
        ]
    ),
])
def test_construct_bsd_messages(tc_unittest, message_parts, message_counter, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.construct_bsd_messages(message_parts, message_counter) == expected_result


@pytest.mark.parametrize("message_part, message_part_counter, expected_result", [
    (
        "hostname",  # we need various hostnames
        2,  # create 2 messages, with 2 different hostnames
        [
            '<38>Jun  1 08:05:04 random_hostname-1 testprogram[9999]: test message - árvíztűrő tükörfúrógép\n',
            '<38>Jun  1 08:05:04 random_hostname-2 testprogram[9999]: test message - árvíztűrő tükörfúrógép\n'
        ],
    ),
])
def test_construct_messages_with_random_message_parts(tc_unittest, message_part, message_part_counter, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.construct_messages_with_various_message_parts(message_part=message_part,
                                                                           message_part_counter=message_part_counter) == expected_result
