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

from src.buffer_io.message_parser import MessageParser
from src.driver_io.file.file_io import FileIO
from src.buffer_io.single_line_parser import SingleLineParser

class SyslogNgConsoleLog(object):
    def __init__(self, logger_factory):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SyslogNgConsoleLog")
        self.stderr = None
        self.message_parser = MessageParser(logger_factory)
        self.single_line_parser = SingleLineParser(logger_factory)
        self.syslog_ng_start_message = ["syslog-ng starting up;"]
        self.syslog_ng_stop_message = ["syslog-ng shutting down"]
        self.syslog_ng_reload_messages = [
            "New configuration initialized",
            "Configuration reload request received, reloading configuration",
            "Configuration reload finished"
        ]
        self.unexpected_patterns = [
            "error",
            "Error",
            "ERROR",
            "warning",
            "Warning",
            "Included file was skipped",
            "Plugin module not found"
        ]

    def wait_for_start_message(self, stderr_file_path):
        return self.wait_for_messages_in_console_log(self.syslog_ng_start_message, stderr_file_path)

    def wait_for_stop_message(self, stderr_file_path):
        return self.wait_for_messages_in_console_log(self.syslog_ng_stop_message, stderr_file_path)

    def wait_for_reload_message(self, stderr_file_path):
        return self.wait_for_messages_in_console_log(self.syslog_ng_reload_messages, stderr_file_path)

    def wait_for_messages_in_console_log(self, expected_messages, stderr_file_path):
        if not self.stderr:
            self.stderr = FileIO(self.logger_factory, stderr_file_path)
            self.stderr.wait_for_creation()

        console_log_messages = self.message_parser.pop_messages(self.stderr.read, self.single_line_parser, counter=0)
        console_log_content = "".join(console_log_messages)

        result = []
        for expected_message in expected_messages:
            result.append(expected_message in console_log_content)
        return all(result)

    def check_for_unexpected_messages(self, stderr_file_path):
        self.stderr = FileIO(self.logger_factory, stderr_file_path)
        console_log_messages = self.message_parser.peek_messages(self.stderr.read, self.single_line_parser, counter=0)
        for unexpected_pattern in self.unexpected_patterns:
            for console_log_message in console_log_messages:
                if unexpected_pattern in console_log_message:
                    self.logger.error("Found unexpected message in console log: {}".format(console_log_message))
                    assert False

    def dump_stderr(self, stderr_file_path, last_n_lines=10):
        self.stderr = FileIO(self.logger_factory, stderr_file_path)
        console_log_messages = self.message_parser.peek_messages(self.stderr.read, self.single_line_parser, counter=0)
        self.logger.info("".join(console_log_messages[-last_n_lines:]))
