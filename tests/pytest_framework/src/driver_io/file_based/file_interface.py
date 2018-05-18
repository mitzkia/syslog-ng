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

from src.driver_io.file_based.file import File
from src.driver_io.file_based.wait_for_event import FileWaitForEvent


class FileInterface(object):

    def __init__(self, logger_factory=None):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("FileInterface")

    def read_content(self, file_path, expected_message_counter=1):
        file_manager = FileWaitForEvent(self.logger_factory, file_path)
        file_manager.wait_for_creation()
        file_content = file_manager.bufferio.pop_msgs(file_manager.read, expected_message_counter)
        self.logger.info(
            "Content received:"
            + "\n>>>From path:[{}]\n".format(file_path)
            + "\n>>>Content:[{}]".format("".join(file_content))
        )
        return file_content

    def write_content(self, file_path, content, open_mode="a+", normalize_line_endings=True):
        file_manager = File(self.logger_factory, file_path)
        self.logger.info(
            "Content written:" + "\n>>>From path:[{}]\n".format(file_path) + "\n>>>Content:[{}]".format(content)
        )
        file_manager.write(content=content, open_mode=open_mode, normalize_line_endings=normalize_line_endings)
