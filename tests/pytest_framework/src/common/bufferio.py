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

from src.common.blocking import wait_until_true


class BufferIO(object):

    def __init__(self):
        self.buffer = ""
        self.msg_list = []

    def buffering_messages(self, read):
        content = read()
        if content:
            if isinstance(content, bytes):
                self.buffer += content.decode("utf-8")
            else:
                self.buffer += content

    def parsing_messages(self, parse_rule="\n"):
        if parse_rule == "\n":
            for chunk in list(self.buffer.splitlines(keepends=True)):
                if chunk.endswith(parse_rule):
                    self.msg_list.append(chunk)
                    self.buffer = self.buffer.replace(chunk, "", 1)
            return True
        assert False, "Not yet supported parse_rule: {}".format(parse_rule)

    def buffer_and_parse(self, read, number_of_requested_messages):
        self.buffering_messages(read)
        self.parsing_messages()
        return self.is_requested_messages_under_parsed_messages(number_of_requested_messages)

    def pop_msg(self, read):
        popped_message = self.pop_msgs(read, number_of_requested_messages=1)
        if isinstance(popped_message, list) and popped_message:
            return popped_message[0]
        return ""

    def pop_msgs(self, read, number_of_requested_messages=0):
        wait_until_true(self.buffer_and_parse, read, number_of_requested_messages)
        if number_of_requested_messages == 0:
            number_of_requested_messages = len(self.msg_list)
        final_msg_list = self.msg_list[0:number_of_requested_messages]
        self.msg_list = self.msg_list[number_of_requested_messages:]
        return final_msg_list

    def peek_msg(self, read):
        return self.peek_msgs(read, number_of_requested_messages=1)[0]

    def peek_msgs(self, read, number_of_requested_messages=0):
        wait_until_true(self.buffer_and_parse, read, number_of_requested_messages)
        if number_of_requested_messages == 0:
            number_of_requested_messages = len(self.msg_list)
        return self.msg_list[0:number_of_requested_messages]

    def is_msg_list_empty(self):
        return self.msg_list == []

    def is_buffer_empty(self):
        return self.buffer == ""

    def is_requested_messages_under_parsed_messages(self, number_of_requested_messages):
        return len(self.msg_list) >= number_of_requested_messages

    # def buffering_and_is_number_of_requested_messages_in_buffer(self, read, number_of_requested_messages):
    #     self.buffering_messages(read)
    #     return number_of_requested_messages == self.buffer.count("\n")
