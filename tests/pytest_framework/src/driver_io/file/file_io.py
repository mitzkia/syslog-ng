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

from src.driver_io.file.file import File

class FileIO(File):
    def __init__(self, logger_factory, file_path):
        super(FileIO, self).__init__(logger_factory, file_path)
        self.logger = logger_factory.create_logger("FileIO")
        self.file_reader_object = None
        self.file_writer_object = None
        self.file_rewriter_object = None

    def read(self, position=None):
        if not self.file_reader_object:
            self.file_reader_object = self.open_file(mode="r")

        if position is not None:
            self.file_reader_object.seek(position)

        content = self.file_reader_object.read()
        return content

    def write(self, content):
        if not self.file_writer_object:
            self.file_writer_object = self.open_file(mode="a+")

        self.file_writer_object.write(content)
        self.file_writer_object.flush()

    def rewrite(self, content):
        self.file_rewriter_object = self.open_file(mode="w+")

        self.file_rewriter_object.write(content)
        self.file_rewriter_object.flush()
