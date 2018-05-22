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

# -*- coding: utf-8 -*-
import pytest
from src.buffer_io.message_parser import MessageParser
from src.buffer_io.single_line_parser import SingleLineParser
from src.common import blocking
blocking.MONITORING_TIME = 0.1

@pytest.mark.parametrize("input_message_counter, requested_message_counter, expected_result", [
    (
        1,
        1,
        True
    ),
    (
        1,
        2,
        False
    ),
    (
        5,
        0,
        False
    )
])
def test_buffer_and_parse(tc_unittest, input_message_counter, requested_message_counter, expected_result):
    message_parser = MessageParser(tc_unittest.get_fake_logger_factory())
    single_line_parser = SingleLineParser(tc_unittest.get_fake_logger_factory())

    input_content = tc_unittest.get_utf8_test_messages(input_message_counter)
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)

    assert message_parser.buffer_and_parse(file_reader_object.read, single_line_parser, requested_message_counter) is expected_result
    if input_message_counter == 1:
        assert single_line_parser.msg_list == [input_content]
    else:
        assert single_line_parser.msg_list == input_content.splitlines(True)

def test_multiple_buffer_and_parse(tc_unittest):
    # Testing self.buffer_io.read_chunk is used instead of self.buffer_io.saved_buffer
    message_parser = MessageParser(tc_unittest.get_fake_logger_factory())
    single_line_parser = SingleLineParser(tc_unittest.get_fake_logger_factory())

    input_content = tc_unittest.get_utf8_test_messages(2)
    file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)
    assert message_parser.buffer_and_parse(file_reader_object.read, single_line_parser, 0) is False

    file_writer_object.write(input_content)
    file_writer_object.flush()
    assert message_parser.buffer_and_parse(file_reader_object.read, single_line_parser, 0) is False
    assert single_line_parser.msg_list == input_content.splitlines(True)*2

@pytest.mark.parametrize("input_message, requested_message_counter, popped_message, msg_list_content, buffer_content", [
    (  # pop as many as came in buffer
        "test message 1\ntest message 2\n",
        2,
        ["test message 1\n", "test message 2\n"],
        [],
        "",
    ),
    (  # one of the messages not parsable
        "test message 1\ntest message 2",
        2,
        ["test message 1\n"],
        [],
        "test message 2",
    ),
    (  # pop less message than came in buffer
        "test message 1\ntest message 2\n",
        1,
        ["test message 1\n"],
        ["test message 2\n"],
        "",
    ),
    (  # pop more message than came in buffer
        "test message 1\ntest message 2\n",
        10,
        ["test message 1\n", "test message 2\n"],
        [],
        "",
    ),
    (  # pop all messages from buffer, 0 = READ_ALL_MESSAGESS
        "test message 1\ntest message 2\n",
        0,
        ["test message 1\n", "test message 2\n"],
        [],
        "",
    ),
    (  # remain 1 message in buffer and msg list
        "test message 1\ntest message 2\ntest message 3",
        1,
        ["test message 1\n"],
        ["test message 2\n"],
        "test message 3",
    ),
])
def test_pop_messages(tc_unittest, input_message, requested_message_counter, popped_message, msg_list_content, buffer_content):
    message_parser = MessageParser(tc_unittest.get_fake_logger_factory())
    single_line_parser = SingleLineParser(tc_unittest.get_fake_logger_factory())

    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_message)

    if requested_message_counter > input_message.count("\n"):
        with pytest.raises(AssertionError):
            message_parser.pop_messages(file_reader_object.read, single_line_parser, requested_message_counter)
    else:
        assert message_parser.pop_messages(file_reader_object.read, single_line_parser, requested_message_counter) == popped_message
        assert message_parser.buffer_io.saved_buffer == buffer_content
        assert single_line_parser.msg_list == msg_list_content

def test_popping_in_sequence(tc_unittest):
    message_parser = MessageParser(tc_unittest.get_fake_logger_factory())
    single_line_parser = SingleLineParser(tc_unittest.get_fake_logger_factory())

    input_content = tc_unittest.get_utf8_test_messages(counter=10)
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)

    input_content_list = input_content.splitlines(True)
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=2) == input_content_list[0:2]
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=2) == input_content_list[2:4]
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=2) == input_content_list[4:6]
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=2) == input_content_list[6:8]
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=2) == input_content_list[8:10]
    assert message_parser.buffer_io.saved_buffer == ""

def test_writing_popping_in_sequence(tc_unittest):
    message_parser = MessageParser(tc_unittest.get_fake_logger_factory())
    single_line_parser = SingleLineParser(tc_unittest.get_fake_logger_factory())

    test_message = "test message 1\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(test_message)
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=1) == test_message.splitlines(True)

    test_message = "test message 2\ntest message 3\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(test_message)
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=2) == test_message.splitlines(True)

    test_message = "test message 4\ntest message 5\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(test_message)
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=1) == ["test message 4\n"]
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=1) == ["test message 5\n"]

    test_message = "test message 6\ntest message 7\ntest message 8\ntest message 9\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(test_message)
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=0) == test_message.splitlines(True)

    test_message = "test message 10\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(test_message)
    assert message_parser.pop_messages(file_reader_object.read, single_line_parser, counter=1) == test_message.splitlines(True)

def test_peek_messages(tc_unittest):
    message_parser = MessageParser(tc_unittest.get_fake_logger_factory())
    single_line_parser = SingleLineParser(tc_unittest.get_fake_logger_factory())

    test_message = "test message 2\ntest message 3\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(test_message)
    assert message_parser.peek_messages(file_reader_object.read, single_line_parser, counter=2) == test_message.splitlines(True)
    assert message_parser.buffer_io.saved_buffer == test_message
    assert single_line_parser.msg_list == test_message.splitlines(True)
