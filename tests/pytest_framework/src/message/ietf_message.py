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


class IETFMessage(object):
    def __init__(self, default_message_parts):
        self.default_message_parts = {
            "priority": default_message_parts.priority,
            "syslog_protocol_version": default_message_parts.syslog_protocol_version,
            "iso_timestamp": default_message_parts.iso_timestamp,
            "hostname": default_message_parts.hostname,
            "program": default_message_parts.program,
            "pid": default_message_parts.pid,
            "message_id": default_message_parts.message_id,
            "sdata": default_message_parts.sdata,
            "message": default_message_parts.message
        }
        self.iso_timestamp_regexp_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}+[0-9]{2}:[0-9]{2}"
        self.bom_pattern = '\ufeff'

    def construct_message(self, message_parts, skip_msg_length=False):
        message = ""
        if "priority" in message_parts:
            message += "<{}>".format(message_parts["priority"])
        if "syslog_protocol_version" in message_parts:
            message += "{} ".format(message_parts["syslog_protocol_version"])
        if "iso_timestamp" in message_parts:
            message += "{} ".format(message_parts["iso_timestamp"])
        if "hostname" in message_parts:
            message += "{} ".format(message_parts["hostname"])
        if "program" in message_parts:
            message += "{} ".format(message_parts["program"])
        if "pid" in message_parts:
            message += "{} ".format(message_parts["pid"])
        if "message_id" in message_parts:
            message += "{} ".format(message_parts["message_id"])
        if "sdata" in message_parts:
            message += '{} '.format(message_parts["sdata"])
        if "message" in message_parts:
            message += "{}{}".format(self.bom_pattern, message_parts["message"])
        if not message_parts["message"].endswith("\n"):
            message += "\n"
        if not skip_msg_length:
            message_length = len(message.encode('utf-8'))
            message = "{} {}".format(message_length, message)
        else:
            message = "{}".format(message)
        return message

    def construct_regexp_message(self, message_parts, skip_msg_length):
        return re.compile(self.construct_message(message_parts, skip_msg_length))
