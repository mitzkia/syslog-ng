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

class BufferIO(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("BufferIO")
        self.saved_buffer = ""
        self.read_chunk = ""
        self.eof = False

    def buffering(self, read):
        self.read_chunk = read()
        if self.is_new_chunk():
            self.saved_buffer += self.read_chunk
        elif (not self.is_new_chunk()) and (not self.is_buffer_empty()):
            self.eof = True

    def delete_chars_from_beginning_buffer(self, last_char_index):
        self.saved_buffer = self.saved_buffer[last_char_index:]

    def reset_eof(self):
        self.eof = False

    def is_new_chunk(self):
        return self.read_chunk != ""

    def is_buffer_empty(self):
        return self.saved_buffer == ""
