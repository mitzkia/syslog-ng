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

import os
import shutil
import stat


class File(object):
    def __init__(self, logger_factory, file_path):
        self.file_path = file_path
        self.logger = logger_factory.create_logger("File")
        self.file_object = None

    def is_file_exist(self):
        return os.path.exists(self.file_path)

    def is_regular_file(self):
        return stat.S_ISREG(os.stat(self.file_path).st_mode)

    def is_named_pipe(self):
        return stat.S_ISFIFO(os.stat(self.file_path).st_mode)

    def copy_file(self, destination_path):
        return shutil.copyfile(self.file_path, destination_path)

    def move_file(self, destination_path):
        return shutil.move(self.file_path, destination_path)

    def delete_file(self):
        return os.unlink(self.file_path)

    def get_number_of_lines(self):
        with open(self.file_path, 'r') as file_object:
            return file_object.read().count("\n")

    def get_size(self):
        return os.stat(self.file_path).st_size

    def get_last_modification_time(self):
        return os.stat(self.file_path).st_mtime

    def read(self):
        if not self.file_object:
            self.file_object = open(self.file_path, 'r')
        return self.file_object.read()

    def write(self, content, open_mode, normalize_line_endings):
        with open(self.file_path, open_mode) as file_object:
            if isinstance(content, list):
                for message in content:
                    if normalize_line_endings:
                        file_object.write(self.normalize_line_endings(message))
                    else:
                        file_object.write(message)
            else:
                if normalize_line_endings:
                    file_object.write(self.normalize_line_endings(content))
                else:
                    file_object.write(content)

    def dump_content(self):
        self.logger.info(self.read())

    @staticmethod
    def normalize_line_endings(line):
        if not line.endswith("\n"):
            line += "\n"
        return line
