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
from src.driver_io.file_based.file import File
from src.common.blocking import wait_until_true
from src.common.bufferio import BufferIO


class FileWaitForEvent(File):
    def __init__(self, logger_factory, file_path):
        super().__init__(logger_factory, file_path)
        self.bufferio = BufferIO()
        self.logger = logger_factory.create_logger("FileWaitForEvent")

    def wait_for_creation(self):
        if not self.file_object:
            result_file_has_created = wait_until_true(self.is_file_exist)
            file_size = wait_until_true(self.get_size)
            self.logger.write_message_based_on_value("File created, file_path: [{}]".format(self.file_path), result_file_has_created)
            return result_file_has_created and (file_size > 0)
        return True

    def wait_for_number_of_lines(self, expected_lines):
        file_creation_result = self.wait_for_creation()
        found_expected_lines = wait_until_true(self.bufferio.buffering_and_is_number_of_requested_messages_in_buffer, self.read, expected_lines)
        return file_creation_result and found_expected_lines

    def wait_for_message(self, expected_message):
        file_creation_result = self.wait_for_creation()
        return file_creation_result and wait_until_true(self.wait_for_message_in_buffer, expected_message)

    def wait_for_message_in_buffer(self, expected_message):
        re_pattern = re.compile(expected_message)
        while not re_pattern.match(self.bufferio.pop_msg(self.read)):
            if self.bufferio.is_msg_list_empty():
                return False
        return True
