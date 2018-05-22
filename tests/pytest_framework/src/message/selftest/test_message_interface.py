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

import socket
import pytest
from src.message.message_interface import MessageInterface


@pytest.mark.parametrize(
    "message_parts, default_message_parts, expected_result", [({"priority": "38"}, {"priority": "38"}, None)]
)
def test_validate_message_parts(tc_unittest, message_parts, default_message_parts, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.validate_message_parts(message_parts, default_message_parts) is expected_result


@pytest.mark.parametrize(
    "message_parts, default_message_parts, expected_result",
    [
        (
            {"priority": "42"}, {"priority": "38"}, {"priority": "42"}  # came from user  # default value
        ),  # user value overwrites default value
        ({"priority": "skip"}, {"priority": "38"}, {}),  # came from user  # default value  # skip the message part
        (
            {"hostname": "testhostname"},  # came from user
            {"priority": "38", "hostname": "otherhostname"},  # default values
            {"hostname": "testhostname", "priority": "38"},
        ),  # using default value, and overwriting default value
    ],
)
def test_set_message_parts(tc_unittest, message_parts, default_message_parts, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.set_message_parts(message_parts, default_message_parts) == expected_result


@pytest.mark.parametrize(
    "message_parts, message_counter, expected_result",
    [
        (
            {},  # use all default values
            1,  # create 1 message
            [
                "<38>Jun  1 08:05:04 {} testprogram[9999]: test message - árvíztűrő tükörfúrógép\n".format(
                    socket.gethostname()
                )
            ],
        ),
        (
            {},  # use all default values
            2,  # create 2 messages
            [
                "<38>Jun  1 08:05:04 {} testprogram[9999]: test message - árvíztűrő tükörfúrógép\n".format(
                    socket.gethostname()
                ),
                "<38>Jun  1 08:05:04 {} testprogram[9999]: test message - árvíztűrő tükörfúrógép\n".format(
                    socket.gethostname()
                ),
            ],
        ),
        (
            {
                "priority": "42",
                "bsd_timestamp": "Dec  1 09:06:32",
                "hostname": "randomhost",
                "program": "randomprogram",
                "pid": "9999",
                "message": "test message",
            },  # overwrite very values
            2,  # create 2 messages
            [
                "<42>Dec  1 09:06:32 randomhost randomprogram[9999]: test message\n",
                "<42>Dec  1 09:06:32 randomhost randomprogram[9999]: test message\n",
            ],
        ),
        (
            {
                "priority": "skip",
                "bsd_timestamp": "skip",
                "hostname": "skip",
                "program": "skip",
                "pid": "skip",
                "message": "test message",
            },  # skipping some message parts
            1,  # create 1 message
            ["test message\n"],
        ),
    ],
)
def test_construct_bsd_messages(tc_unittest, message_parts, message_counter, expected_result):
    message_interface = MessageInterface(tc_unittest.fake_logger_factory())
    assert message_interface.construct_bsd_messages(message_parts, message_counter) == expected_result
