#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from src.message.log_message import LogMessage

class MessageBuilder(object):
    def __init__(self):
        self.log_message = LogMessage()

        # common message fields
        self.default_priority = "38"
        self.default_hostname = socket.gethostname()
        self.default_static_hostname = "mymachine.example.com"
        self.default_program = "testprogram"
        self.default_pid = "9999"
        self.default_message = "test message - árvíztűrő tükörfúrógép"

        # BSD specific message fields
        self.default_bsd_timestamp = "Jun  1 08:05:04"

        # IETF specific message fields
        self.default_syslog_protocol_version = "1"
        self.default_iso_timestamp = "2017-06-01T08:05:04+02:00"
        self.default_iso_timestamp2 = "2003-10-11T22:14:15.003Z"
        self.default_iso_timestamp3 = "20180531T235405Z"
        self.default_message_id = "-"
        self.default_sdata = '[meta sequenceId="1"]'

    def set_undefined_message_fields(self, message_fields):
        for message_field in message_fields:
            if not getattr(self.log_message, "{}_value".format(message_field)):
                setattr(self.log_message, "{}_value".format(message_field), getattr(self, 'default_{}'.format(message_field)))

    def get_raw_message(self):
        return self.log_message.get_raw_message()

    def get_message(self):
        return self.log_message.get_message()

    def get_messages(self, counter):
        return self.log_message.get_messages(counter)

    # Common message fields
    def priority(self, priority):
        self.log_message.priority(priority)
        return self

    def remove_priority(self):
        self.log_message.priority("disabled")
        return self

    def hostname(self, hostname):
        self.log_message.hostname(hostname)
        return self

    def program(self, program):
        self.log_message.program(program)
        return self

    def pid(self, pid):
        self.log_message.pid(pid)
        return self

    def message(self, message):
        self.log_message.message(message)
        return self
