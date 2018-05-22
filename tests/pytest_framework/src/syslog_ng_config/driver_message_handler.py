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

from src.message.message_interface import MessageInterface

class DriverMessageHandler(object):
    def __init__(self, logger_factory):
        self.message_interface = MessageInterface(logger_factory)

    def generate_output_message(self, message, message_header_fields, counter):
        message_field = {"message": message}
        if message_header_fields:
            message_header_fields = {**message_header_fields, **{"priority": "skip"}}
        else:
            message_header_fields = {**{"priority": "skip"}}
        message_parts = {**message_field, **message_header_fields}
        return self.message_interface.construct_bsd_messages(message_parts, counter)

    def generate_default_output_message(self, counter=1):
        return self.message_interface.construct_bsd_messages({"priority": "skip"}, counter)
