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

from src.syslog_ng_config.statements.statement import Statement

class SourceDriver(Statement):
    def __init__(self, logger_factory, instance_parameters, native_driver_io_ref, empty_driver_content):
        super(SourceDriver, self).__init__(logger_factory, instance_parameters, empty_driver_content)
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SourceDriver")
        self.native_driver_io_ref = native_driver_io_ref

    def write_message(self, message):
        if not self.native_driver_io:
            self.native_driver_io = self.native_driver_io_ref(self.logger_factory, self.mandatory_option_value)
        self.native_driver_io.write(message.get_raw_message())
        self.logger.print_io_content(self.mandatory_option_value, message.get_raw_message(), "Content has been written to")

    def write_messages(self, messages):
        for message in messages:
            self.write_message(message)
