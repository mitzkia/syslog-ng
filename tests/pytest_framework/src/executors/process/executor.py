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
from src.executors.process.common import ProcessCommon


class ProcessExecutor(ProcessCommon):
    def __init__(self, logger_factory):
        ProcessCommon.__init__(self, logger_factory)
        self.logger = logger_factory.create_logger("ProcessExecutor")
        self.process_object = None
        self.pid = None
        self.command_of_process = None

    def start(self, command_of_process, stdout, stderr):
        self.command_of_process = command_of_process
        self.logger.info("Following process will be started: [{}]".format(" ".join(command_of_process)))
        stdout_fd = open(stdout, 'a')
        stderr_fd = open(stderr, 'a')
        self.process_object = psutil.Popen(command_of_process, stderr=stderr_fd, stdout=stdout_fd)
        self.pid = self.process_object.pid
        self.logger.info("Process started with pid [{}]".format(self.pid))
        return self.process_object
