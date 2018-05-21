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

class DriverIOHandler(object):
    def __init__(self, driver_io):
        self.driver_io = driver_io

    def write_content(self, file_path, content):
        return self.driver_io.write_content(file_path, content)

    def read_msg(self, file_path):
        return self.driver_io.read_msg(file_path)

    def read_msgs(self, file_path, message_counter):
        return self.driver_io.read_msgs(file_path, message_counter)

    def read_all_msgs(self, file_path):
        return self.driver_io.read_all_msgs(file_path)
