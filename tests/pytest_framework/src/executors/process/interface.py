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

from src.executors.process.executor import ProcessExecutor
from src.executors.process.signal_handler import ProcessSignalHandler


class ProcessInterface(ProcessExecutor, ProcessSignalHandler):
    def __init__(self, logger_factory):
        ProcessExecutor.__init__(self, logger_factory)
        ProcessSignalHandler.__init__(self, logger_factory)
        self.process_object = None
        self.pid = None
        self.exit_code = None

    def get_process(self):
        return self.process_object

    def get_pid(self):
        return self.pid

    def get_exit_code(self):
        return self.exit_code
