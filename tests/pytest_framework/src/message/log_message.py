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

class LogMessage(object):
    def __init__(self, message=None):
        self.priority_value = ""
        self.bsd_timestamp_value = ""
        self.hostname_value = ""
        self.program_value = ""
        self.pid_value = ""
        if message:
            self.message(message)
        else:
            self.message_value = ""

        self.syslog_protocol_version_value = ""
        self.iso_timestamp_value = ""
        self.message_id_value = ""
        self.sdata_value = ""
        self.raw_message = ""

    def priority(self, priority):
        self.priority_value = priority
        return self

    def bsd_timestamp(self, bsd_timestamp):
        self.bsd_timestamp_value = bsd_timestamp
        return self

    def hostname(self, hostname):
        self.hostname_value = hostname
        return self

    def program(self, program):
        self.program_value = program
        return self

    def pid(self, pid):
        self.pid_value = pid
        return self

    def message(self, message):
        self.message_value = message
        return self

    def syslog_protocol_version(self, syslog_protocol_version):
        self.syslog_protocol_version_value = syslog_protocol_version
        return self

    def iso_timestamp(self, iso_timestamp):
        self.iso_timestamp_value = iso_timestamp
        return self

    def message_id(self, message_id):
        self.message_id_value = message_id
        return self

    def sdata(self, sdata):
        self.sdata_value = sdata
        return self

    def get_raw_message(self):
        return self.raw_message

    def get_message(self):
        return [self.raw_message]

    def get_messages(self, counter):
        return self.get_message() * counter

    def build(self):
        self.raw_message = ""
        if self.priority_value:
            self.raw_message += "<{}>".format(self.priority_value)
        if self.bsd_timestamp_value:
            self.raw_message += "{} ".format(self.bsd_timestamp_value)
        if self.hostname_value:
            self.raw_message += "{} ".format(self.hostname_value)
        if self.program_value:
            self.raw_message += "{} ".format(self.program_value)
        if self.pid_value:
            self.raw_message += "[{}]:".format(self.pid_value)
        if self.message_value:
            self.raw_message += "{}\n".format(self.message_value)
        return self
