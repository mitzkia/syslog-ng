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
from src.common.bufferio import BufferIO
from src.common import blocking

blocking.MONITORING_TIME = 0.5


def get_empty_content():
    return b""


def get_content_without_new_line_at_the_end():
    return b"""new message 1
new message 2
new message 3"""


def get_content_with_new_line_at_the_end():
    return b"""new message 1
new message 2
new message 3
"""


def get_content_with_same_messages_without_new_line_at_the_end():
    return b"""new message 1
new message 1
new message 1"""


def get_dependencies(tc_unittest):
    bufferio = BufferIO()
    return bufferio, tc_unittest.fake_path()


def test_buffering_messages_read_new_content(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    bufferio.buffering_messages(fake_path.read)
    assert bufferio.buffer == get_content_without_new_line_at_the_end().decode("utf-8")
    fake_path.close()


def test_buffering_messages_read_new_content_but_the_buffer_already_contains_content(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    bufferio.buffer = "first message in buffer\n"
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    bufferio.buffering_messages(fake_path.read)
    assert bufferio.buffer == "first message in buffer\n" + get_content_without_new_line_at_the_end().decode("utf-8")
    fake_path.close()


def test_buffering_messages_read_empty_content(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_empty_content())
    fake_path.seek(0)
    bufferio.buffering_messages(fake_path.read)
    assert bufferio.buffer == get_empty_content().decode("utf-8")
    fake_path.close()


def test_buffering_messages_multiple_times(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    bufferio.buffering_messages(fake_path.read)
    assert (
        bufferio.buffer
        == get_content_without_new_line_at_the_end().decode("utf-8")
        + get_content_without_new_line_at_the_end().decode("utf-8")
    )
    fake_path.close()


def test_parsing_messages_got_messages_with_and_without_newlines(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    bufferio.buffer = get_content_without_new_line_at_the_end().decode("utf-8")
    bufferio.parsing_messages()
    assert bufferio.msg_list == ["new message 1\n", "new message 2\n"]
    assert bufferio.buffer == "new message 3"
    fake_path.close()


def test_parsing_messages_got_same_message_multiple_times(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    bufferio.buffer = get_content_with_same_messages_without_new_line_at_the_end().decode("utf-8")
    bufferio.parsing_messages()
    assert bufferio.msg_list == ["new message 1\n", "new message 1\n"]
    assert bufferio.buffer == "new message 1"
    fake_path.close()


def test_parsing_messages_got_every_message_with_newline(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    bufferio.buffer = get_content_with_new_line_at_the_end().decode("utf-8")
    bufferio.parsing_messages()
    assert bufferio.msg_list == get_content_with_new_line_at_the_end().decode("utf-8").splitlines(keepends=True)
    assert bufferio.buffer == ""
    fake_path.close()


def test_parsing_messages_multiple_times(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    bufferio.buffer = get_content_with_new_line_at_the_end().decode("utf-8")
    bufferio.parsing_messages()
    bufferio.buffer = get_content_with_new_line_at_the_end().decode("utf-8")
    bufferio.parsing_messages()
    assert (
        bufferio.msg_list
        == get_content_with_new_line_at_the_end().decode("utf-8").splitlines(keepends=True)
        + get_content_with_new_line_at_the_end().decode("utf-8").splitlines(keepends=True)
    )
    assert bufferio.buffer == ""
    fake_path.close()


@pytest.mark.parametrize(
    "number_of_requested_messages, buffer_and_parse_result, msg_list, buffer",
    [
        (0, True, ["new message 1\n", "new message 2\n"], "new message 3"),
        (1, True, ["new message 1\n", "new message 2\n"], "new message 3"),
        (2, True, ["new message 1\n", "new message 2\n"], "new message 3"),
        (3, False, ["new message 1\n", "new message 2\n"], "new message 3"),
    ],
)
def test_buffer_and_parse(tc_unittest, number_of_requested_messages, buffer_and_parse_result, msg_list, buffer):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    assert bufferio.buffer_and_parse(fake_path.read, number_of_requested_messages) is buffer_and_parse_result
    assert bufferio.msg_list == msg_list
    assert bufferio.buffer == buffer
    fake_path.close()


@pytest.mark.parametrize(
    "number_of_requested_messages, pop_msgs_result, msg_list, buffer",
    [
        (-1, ["new message 1\n", "new message 2\n"], [], "new message 3"),  # means get all messages from buffer
        (0, [], ['new message 1\n', 'new message 2\n'], "new message 3"),
        (1, ["new message 1\n"], ["new message 2\n"], "new message 3"),
        (2, ["new message 1\n", "new message 2\n"], [], "new message 3"),
        (3, ["new message 1\n", "new message 2\n"], [], "new message 3"),
    ],
)
def test_pop_msgs(tc_unittest, number_of_requested_messages, pop_msgs_result, msg_list, buffer):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    assert bufferio.pop_msgs(fake_path.read, number_of_requested_messages) == pop_msgs_result
    assert bufferio.msg_list == msg_list
    assert bufferio.buffer == buffer
    fake_path.close()


def test_pop_msg_when_there_is_no_new_line_at_the_end(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    assert bufferio.pop_msg(fake_path.read) == "new message 1\n"
    assert bufferio.msg_list == ["new message 2\n"]
    assert bufferio.buffer == "new message 3"
    assert bufferio.pop_msg(fake_path.read) == "new message 2\n"
    assert bufferio.msg_list == []
    assert bufferio.buffer == "new message 3"
    assert bufferio.pop_msg(fake_path.read) == ""
    assert bufferio.msg_list == []
    assert bufferio.buffer == "new message 3"
    fake_path.close()


@pytest.mark.parametrize(
    "number_of_requested_messages, peek_msgs_result, msg_list, buffer",
    [
        (
            -1,  # means get all messages from buffer
            ["new message 1\n", "new message 2\n"],
            ["new message 1\n", "new message 2\n"],
            "new message 3",
        ),
        (
            0,
            [],
            ["new message 1\n", "new message 2\n"],
            "new message 3",
        ),
        (1, ["new message 1\n"], ["new message 1\n", "new message 2\n"], "new message 3"),
        (2, ["new message 1\n", "new message 2\n"], ["new message 1\n", "new message 2\n"], "new message 3"),
        (3, ["new message 1\n", "new message 2\n"], ["new message 1\n", "new message 2\n"], "new message 3"),
    ],
)
def test_peek_msgs(tc_unittest, number_of_requested_messages, peek_msgs_result, msg_list, buffer):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    assert bufferio.peek_msgs(fake_path.read, number_of_requested_messages) == peek_msgs_result
    assert bufferio.msg_list == msg_list
    assert bufferio.buffer == buffer
    fake_path.close()


def test_peek_msg_when_there_is_no_new_line_at_the_end(tc_unittest):
    bufferio, fake_path = get_dependencies(tc_unittest)
    fake_path.write(get_content_without_new_line_at_the_end())
    fake_path.seek(0)
    assert bufferio.peek_msg(fake_path.read) == "new message 1\n"
    assert bufferio.msg_list == ["new message 1\n", "new message 2\n"]
    assert bufferio.buffer == "new message 3"
    assert bufferio.peek_msg(fake_path.read) == "new message 1\n"
    assert bufferio.msg_list == ["new message 1\n", "new message 2\n"]
    assert bufferio.buffer == "new message 3"
    assert bufferio.peek_msg(fake_path.read) == "new message 1\n"
    assert bufferio.msg_list == ["new message 1\n", "new message 2\n"]
    assert bufferio.buffer == "new message 3"
    fake_path.close()
