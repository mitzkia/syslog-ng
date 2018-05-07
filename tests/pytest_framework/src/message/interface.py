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
import socket
from src.message.bsd_message import BSDMessage
from src.message.ietf_message import IETFMessage


class DefaultMessageParts(object):
    @property
    def priority(self):
        return "38"

    @property
    def syslog_protocol_version(self):
        return "1"

    @property
    def bsd_timestamp(self):
        return "Jun  1 08:05:04"

    @property
    def iso_timestamp(self):
        return "2017-06-01T08:05:04+02:00"

    @property
    def hostname(self):
        return socket.gethostname()

    @property
    def program(self):
        return "testprogram"

    @property
    def pid(self):
        return "9999"

    @property
    def message_id(self):
        return "-"

    @property
    def sdata(self):
        return '[meta sequenceId="1"]'

    @property
    def message(self):
        return "test message - árvíztűrő tükörfúrógép"

class MessageInterface(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("MessageInterface")
        self.default_message_parts = DefaultMessageParts()
        self.bsd_message = BSDMessage(self.default_message_parts)
        self.ietf_message = IETFMessage(self.default_message_parts)
        self.custom_message_pattern = {
            "hostname": "random_hostname",
            "program": "random_program",
        }

    def construct_bsd_messages(self, message, message_header_fields, message_counter=1, skip_msg_length=None):
        message_parts = self.merge_message_parts(message, message_header_fields)
        return self.construct_messages(self.bsd_message, message_parts, message_counter, skip_msg_length)

    def construct_ietf_messages(self, message, message_header_fields, message_counter=1, skip_msg_length=False):
        message_parts = self.merge_message_parts(message, message_header_fields)
        return self.construct_messages(self.ietf_message, message_parts, message_counter, skip_msg_length)

    def construct_messages(self, message_format, message_parts, message_counter, skip_msg_length):
        self.validate_message_parts(message_parts, message_format.default_message_parts)
        merged_message_parts = self.set_message_parts(message_parts, message_format.default_message_parts)
        messages = []
        for dummy_actual_counter in range(1, message_counter + 1):
            if ("meta" in merged_message_parts.keys()) and (merged_message_parts['meta'] == "regexp"):
                messages.append(message_format.construct_regexp_message(merged_message_parts, skip_msg_length))
            else:
                messages.append(message_format.construct_message(merged_message_parts, skip_msg_length))
        if ("meta" in merged_message_parts.keys()) and (merged_message_parts['meta'] == "regexp"):
            return messages
        return "".join(messages)

    def construct_messages_with_various_message_parts(self, message_part, message_part_counter):
        various_message_parts = []
        for counter in range(1, message_part_counter + 1):
            various_message_parts.append("{}-{}".format(self.custom_message_pattern[message_part], counter))
        generated_messages = []
        for various_message_part in various_message_parts:
            generated_messages.append(
                self.construct_messages(self.bsd_message, {message_part: various_message_part}, message_counter=1, skip_msg_length=None))
        return generated_messages

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
            elif (message_part_name == "bsd_timestamp") and (message_part_value == "regexp"):
                merged_message_parts[message_part_name] = self.bsd_message.bsd_timestamp_regexp_pattern
                merged_message_parts['meta'] = "regexp"
            else:
                merged_message_parts[message_part_name] = message_part_value
        return merged_message_parts

    def merge_message_parts(self, message, message_header_fields):
        message_parts = {}
        if message:
            message_parts = {**message}
        if message_header_fields:
            message_parts = {**message_header_fields}
        return message_parts