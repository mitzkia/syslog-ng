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

class IETFMessageBuilder(MessageBuilder):
    def __init__(self, message=None):
        super(IETFMessageBuilder, self).__init__()
        self.ietf_message_fields = ["priority", "syslog_protocol_version", "iso_timestamp", "hostname", "program", "pid", "message_id", "sdata", "message"]
        if message:
            self.message(message)

    def syslog_protocol_version(self, syslog_protocol_version):
        self.log_message.syslog_protocol_version(syslog_protocol_version)
        return self

    def iso_timestamp(self, iso_timestamp):
        self.log_message.iso_timestamp(iso_timestamp)
        return self

    def message_id(self, message_id):
        self.log_message.message_id(message_id)
        return self

    def sdata(self, sdata):
        self.log_message.sdata(sdata)
        return self

    def build(self, counter=1):
        self.set_undefined_message_fields(self.ietf_message_fields)
        self.build_ietf_message()
        if counter > 1:
            return [self]*counter
        return self

    def build_ietf_message(self):
        self.log_message.raw_message = ""
        self.log_message.raw_message += "<{}>".format(self.log_message.priority_value)
        self.log_message.raw_message += "{}".format(self.log_message.syslog_protocol_version_value)
        self.log_message.raw_message += " {}".format(self.log_message.iso_timestamp_value)
        self.log_message.raw_message += " {}".format(self.log_message.hostname_value)
        self.log_message.raw_message += " {}".format(self.log_message.program_value)
        self.log_message.raw_message += " {}".format(self.log_message.pid_value)
        self.log_message.raw_message += " {}".format(self.log_message.message_id_value)
        self.log_message.raw_message += " {}".format(self.log_message.sdata_value)
        self.log_message.raw_message += " {}\n".format(self.log_message.message_value)
