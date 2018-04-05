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


class Dir(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def is_dir_exist(self):
        return os.path.isdir(self.dir_path)

    def delete_dir(self):
        if self.is_dir_exist():
            os.rmdir(self.dir_path)
        raise Exception("Dir does not exist: {}".format(self.dir_path))

    def create_dir(self):
        if not self.is_dir_exist():
            os.makedirs(self.dir_path)
        raise Exception("Dir already exist: {}".format(self.dir_path))
