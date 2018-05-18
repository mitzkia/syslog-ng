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

import copy
from src.message.bsd_formatter import BSDFormatter
from src.message.ietf_formatter import IETFFormatter


class MessageInterface(object):

    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("MessageInterface")
        self.bsd_formatter = BSDFormatter()
        self.ietf_formatter = IETFFormatter()

    def construct_bsd_messages(self, message_parts, message_counter=1):
        return self.construct_messages(self.bsd_formatter, message_parts, message_counter)

    def construct_ietf_messages(self, message_parts, message_counter=1):
        return self.construct_messages(self.ietf_formatter, message_parts, message_counter)

    def construct_messages(self, message_formatter, message_parts, message_counter):
        self.validate_message_parts(message_parts, message_formatter.default_message_parts)
        merged_message_parts = self.set_message_parts(message_parts, message_formatter.default_message_parts)
        messages = []
        for dummy_actual_counter in range(1, message_counter + 1):
            messages.append(message_formatter.construct_message(merged_message_parts))
        return messages

    @staticmethod
    def validate_message_parts(message_parts, default_message_parts):
        if message_parts and (set(message_parts) - set(default_message_parts)):
            raise Exception("Found unknown message part in: {}".format(message_parts))

    def set_message_parts(self, message_parts, default_message_parts):
        if not message_parts:
            return default_message_parts
        merged_message_parts = copy.deepcopy(default_message_parts)
        for message_part_name, message_part_value in message_parts.items():
            if message_part_value == "skip":
                merged_message_parts.pop(message_part_name)
            else:
                merged_message_parts[message_part_name] = message_part_value
        return merged_message_parts
