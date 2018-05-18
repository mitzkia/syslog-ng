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
import glob
from src.executors.command import CommandExecutor
from src.driver_io.file_based.file import File


class SlngCommandExecutor(object):
    def __init__(self, logger_factory, instance_parameters):
        self.logger_factory = logger_factory
        self.logger = logger_factory.create_logger("SlngCommandExecutor")
        syslog_ng_binary_path = instance_parameters['binary_file_paths']['syslog_ng_binary']
        self.working_dir = instance_parameters['dir_paths']['working_dir']
        config_path = instance_parameters['file_paths']['config_path']
        self.slng_commands = {
            "version": {
                "cmd": [syslog_ng_binary_path, "--version"],
                "stdout": os.path.join(self.working_dir, "slng_version_stdout"),
                "stderr": os.path.join(self.working_dir, "slng_version_stderr")
            },
            "syntax_only": {
                "cmd": [syslog_ng_binary_path, "--enable-core", "--syntax-only", "--cfgfile={}".format(config_path)],
                "stdout": os.path.join(self.working_dir, "slng_syntax_only_stdout"),
                "stderr": os.path.join(self.working_dir, "slng_syntax_only_stderr"),
            },
            "gdb_bt_full": {
                "cmd": ["gdb", "-ex", "bt full", "--batch", syslog_ng_binary_path, "--core"],
                "stdout": os.path.join(self.working_dir, "core_stdout.backtrace"),
                "stderr": os.path.join(self.working_dir, "core_stderr.backtrace")
            }
        }
        self.core_detected = False

    def slng_executor(self, cmd_reference, core_file=None):
        if core_file:
            self.slng_commands[cmd_reference]['cmd'].append(core_file)
        return CommandExecutor(
            self.logger_factory,
            self.slng_commands[cmd_reference]['cmd'],
            stdout=self.slng_commands[cmd_reference]['stdout'],
            stderr=self.slng_commands[cmd_reference]['stderr']
        )

    def is_core_file_exist(self):
        found_core_files = glob.glob(os.path.join(os.getcwd(), "core*"))
        if found_core_files:
            for core_file in found_core_files:
                self.core_detected = True
                self.slng_executor("gdb_bt_full", core_file=core_file)
                File(self.logger_factory, core_file).move_file("{}/".format(self.working_dir))
                raise Exception("syslog-ng core file found and processed")

    def get_version(self):
        version_output = self.slng_executor(cmd_reference="version").get_stdout()
        for version_output_line in version_output.splitlines():
            if "Config version:" in version_output_line:
                return version_output_line.split()[2]
        raise Exception("Can not parse 'Config version' from ./syslog-ng --version")
