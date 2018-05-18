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

from src.driver_io.file_based.wait_for_event import FileWaitForEvent
from src.driver_io.file_based.file import File


class SlngConsoleHandler(object):

    def __init__(self, logger_factory):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SlngConsoleHandler")
        self.syslog_ng_start_message = [".*syslog-ng starting up;"]
        self.syslog_ng_stop_message = [".*syslog-ng shutting down"]
        self.syslog_ng_reload_messages = [
            ".*New configuration initialized",
            ".*Configuration reload request received, reloading configuration",
            ".*Configuration reload finished",
        ]
        self.stderr_file = None

    def wait_for_start_message(self, stderr_file):
        return self.wait_for_console_message(self.syslog_ng_start_message, stderr_file)

    def wait_for_reload_message(self, stderr_file):
        return self.wait_for_console_message(self.syslog_ng_reload_messages, stderr_file)

    def wait_for_stop_message(self, stderr_file):
        return self.wait_for_console_message(self.syslog_ng_stop_message, stderr_file)

    def wait_for_console_message(self, messages, stderr_file):
        if not self.stderr_file:
            self.stderr_file = FileWaitForEvent(self.logger_factory, stderr_file)
        result = []
        for message in messages:
            found_message_in_console_log = self.stderr_file.wait_for_message(expected_message=message)
            result.append(found_message_in_console_log)
        return all(result)

    def dump_console_log(self, stderr_file):
        File(self.logger_factory, stderr_file).dump_content()
