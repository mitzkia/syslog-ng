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

import psutil
from src.common.blocking import wait_until_true


class ProcessCommon(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("ProcessCommon")
        self.process_object = None
        self.pid = None

    def is_process_running(self):
        if self.process_object:
            return self.process_object.is_running()
        return False

    def is_pid_in_process_list(self):
        if self.process_object:
            return psutil.pid_exists(self.pid)
        return False

    def wait_for_pid(self):
        return wait_until_true(self.is_pid_in_process_list)

    def get_opened_file_list(self):
        open_files = self.process_object.open_files()
        if open_files:
            self.logger.error("Found remaining open files: {}".format(open_files))
        return open_files

    def dump_process_information(self):
        self.logger.info("Process information: [{}]".format(str(self.process_object.as_dict())))
