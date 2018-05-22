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

from src.common.path_and_operations import move_file, open_file
from src.common.blocking import wait_until_true

class File(object):
    def __init__(self, logger_factory, file_path):
        self.logger = logger_factory.create_logger("File")
        self.file_path = file_path
        self.file_object = None

    def __del__(self):
        if self.file_object:
            self.file_object.close()
            self.file_object = None

    def is_file_exist(self):
        return self.file_path.exists()

    def get_size(self):
        return self.file_path.stat().st_size

    def delete_file(self):
        self.file_path.unlink()

    def move_file(self, destination_dir):
        return move_file(self.file_path, destination_dir)

    def wait_for_creation(self):
        file_created = wait_until_true(self.is_file_exist)
        self.logger.print_message_based_on_value("File has been created, file_path: [{}]".format(self.file_path), file_created)
        return file_created

    def get_id(self):
        return hex(id(self))

    def get_current_position(self):
        return self.file_object.tell()

    def open_file(self, mode):
        self.file_object = open_file(self.file_path, mode)
        return self.file_object

    def is_closed(self):
        if self.file_object:
            return self.file_object.closed
        return None
