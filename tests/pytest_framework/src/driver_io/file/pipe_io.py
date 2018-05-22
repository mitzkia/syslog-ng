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
import sys
from src.common.path_and_operations import open_pipe
from src.driver_io.file.file import File

class PipeIO(File):
    def __init__(self, logger_factory, file_path):
        super(PipeIO, self).__init__(logger_factory, file_path)
        self.logger = logger_factory.create_logger("PipeIO")
        self.pipe_reader_object = None

    def read(self):
        if not self.pipe_reader_object:
            self.pipe_reader_object = open_pipe(self.file_path, os.O_RDONLY | os.O_NONBLOCK)
        pipe_buffer = ""
        while True:
            try:
                pipe_chunk = os.read(self.pipe_reader_object, 1024)
                if pipe_chunk:
                    if sys.version_info.major == 3:
                        # Working note in python 3: os.read() returns with: <class 'bytes'>
                        pipe_buffer += pipe_chunk.decode()
                    elif sys.version_info.major == 2:
                        # Working note in python 2: os.read() returns with: <type 'str'>
                        pipe_buffer += pipe_chunk.decode("utf8").encode("utf8")
            except OSError:
                # Working note: after read "Resource temporarily unavailable"
                break
        return pipe_buffer
