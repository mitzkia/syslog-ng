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

from src.message.message_builder import MessageBuilder

class BSDMessageBuilder(MessageBuilder):
    def __init__(self, message=None):
        super(BSDMessageBuilder, self).__init__()
        self.bsd_message_fields = ["priority", "bsd_timestamp", "hostname", "program", "pid", "message"]
        if message:
            self.message(message)

    def bsd_timestamp(self, bsd_timestamp):
        self.log_message.bsd_timestamp(bsd_timestamp)
        return self

    def build(self, counter=1):
        self.set_undefined_message_fields(self.bsd_message_fields)
        self.build_bsd_message()
        if counter > 1:
            return [self]*counter
        return self

    def build_bsd_message(self):
        self.log_message.raw_message = ""
        if self.log_message.priority_value != "disabled":
            self.log_message.raw_message += "<{}>".format(self.log_message.priority_value)
        self.log_message.raw_message += "{}".format(self.log_message.bsd_timestamp_value)
        self.log_message.raw_message += " {}".format(self.log_message.hostname_value)
        self.log_message.raw_message += " {}".format(self.log_message.program_value)
        self.log_message.raw_message += "[{}]:".format(self.log_message.pid_value)
        self.log_message.raw_message += " {}\n".format(self.log_message.message_value)
