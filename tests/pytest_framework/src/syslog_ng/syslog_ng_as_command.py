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

from src.syslog_ng.syslog_ng_executor import SyslogNgExecutor

class SyslogNgAsCommand(object):
    def __init__(self, logger_factory, instance_parameters):
        self.syslog_ng_executor = SyslogNgExecutor(logger_factory, instance_parameters)

    def get_version(self):
        version_output = self.syslog_ng_executor.run_command(command_short_name="version")['stdout']
        for version_output_line in version_output.splitlines():
            if "Config version:" in version_output_line:
                return version_output_line.split()[2]
        raise Exception("Can not parse 'Config version' from ./syslog-ng --version")

    def preprocess_into(self):
        return self.syslog_ng_executor.run_command(command_short_name="preprocess_into")
