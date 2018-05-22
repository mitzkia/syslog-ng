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

from src.buffer_io.buffer_io import BufferIO
from src.common.blocking import wait_until_true

class MessageParser(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("MessageParser")
        self.buffer_io = BufferIO(logger_factory)
        self.READ_ALL_MESSAGESS = 0

    def buffer_and_parse(self, read, parser, counter):
        self.buffer_io.buffering(read)
        if self.buffer_io.is_new_chunk():
            parser.parse_buffer(self.buffer_io.read_chunk)
        if counter != self.READ_ALL_MESSAGESS:
            return len(parser.msg_list) >= counter
        return self.buffer_io.eof and (len(parser.msg_list) >= counter)

    def delete_parsed_messages_from_buffer(self, parser):
        self.buffer_io.delete_chars_from_beginning_buffer(parser.get_number_of_parsed_chars())

    def delete_expected_messages_from_parsed_msg_list(self, parser, counter):
        if counter == self.READ_ALL_MESSAGESS:
            counter = len(parser.msg_list)
        final_msg_list = parser.msg_list[0:counter]
        parser.msg_list = parser.msg_list[counter:]
        return final_msg_list

    def pop_messages(self, read, parser, counter):
        self.buffer_io.reset_eof()
        assert wait_until_true(self.buffer_and_parse, read, parser, counter) is True
        self.delete_parsed_messages_from_buffer(parser)
        final_msg_list = self.delete_expected_messages_from_parsed_msg_list(parser, counter)

        return final_msg_list

    def peek_messages(self, read, parser, counter):
        wait_until_true(self.buffer_and_parse, read, parser, counter)

        if counter == self.READ_ALL_MESSAGESS:
            counter = len(parser.msg_list)
        return parser.msg_list[0:counter]
