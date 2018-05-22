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

from src.syslog_ng.syslog_ng_as_command import SyslogNgAsCommand
from src.syslog_ng.syslog_ng_as_process import SyslogNgAsProcess
from src.syslog_ng.syslog_ng_console_log import SyslogNgConsoleLog

class SyslogNg(object):
    def __init__(self, logger_factory, instance_parameters):
        self.instance_parameters = instance_parameters
        self.syslog_ng_console_log = SyslogNgConsoleLog(logger_factory)
        self.syslog_ng_as_process = SyslogNgAsProcess(logger_factory, instance_parameters, self.syslog_ng_console_log)
        self.syslog_ng_as_command = SyslogNgAsCommand(logger_factory, instance_parameters)

    def start(self, config=None, external_tool=None, expected_run=True):
        self.syslog_ng_as_process.start(config, external_tool, expected_run)

    def stop(self):
        self.syslog_ng_as_process.stop()

    def reload(self, config=None):
        self.syslog_ng_as_process.reload(config)

    def restart(self, config):
        self.syslog_ng_as_process.start(config, external_tool=None, expected_run=True)
        self.syslog_ng_as_process.stop()

    def get_version(self):
        return self.syslog_ng_as_command.get_version()

    def get_process_info(self):
        return self.syslog_ng_as_process.get_process_info()
