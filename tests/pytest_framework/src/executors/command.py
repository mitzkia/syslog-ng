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


class CommandExecutor(object):

    def __init__(self, logger_factory, command, stdout, stderr, recreate_output=False):
        self.logger = logger_factory.create_logger("CommandExecutor")
        self.command = command
        self.exit_code = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdout_content = None
        self.stderr_content = None
        self.execute_command(recreate_output)
        self.print_std_outputs()
        self.evaluate_exit_code()

    def execute_command(self, recreate_output):
        self.logger.debug("Following command will be executed: {}".format(" ".join(self.command)))
        if recreate_output:
            stdout_fd = open(self.stdout, "w")
            stderr_fd = open(self.stderr, "w")
        else:
            stdout_fd = open(self.stdout, "a")
            stderr_fd = open(self.stderr, "a")
        with psutil.Popen(self.command, stderr=stderr_fd, stdout=stdout_fd) as proc:
            self.exit_code = proc.wait(timeout=10)
        stdout_fd.close()
        stderr_fd.close()

    def get_stdout(self):
        return self.stdout_content

    def get_stderr(self):
        return self.stderr_content

    def get_exit_code(self):
        return self.exit_code

    def get_all(self):
        return self.exit_code, self.stdout_content, self.stderr_content

    def get_command(self):
        return self.command

    def print_std_outputs(self):
        with open(self.stdout, "r") as stdout_fd, open(self.stderr, "r") as stderr_fd:
            self.stdout_content = stdout_fd.read()
            self.stderr_content = stderr_fd.read()
        self.logger.debug("All Stdout for this command: [{}]".format(self.stdout_content))
        self.logger.debug("All Stderr for this command: [{}]".format(self.stderr_content))

    def evaluate_exit_code(self):
        exit_code_debug_log = "Exit code: [{}]".format(self.exit_code)
        if self.exit_code == 0:
            self.logger.debug(exit_code_debug_log)
        else:
            self.logger.error(exit_code_debug_log)
