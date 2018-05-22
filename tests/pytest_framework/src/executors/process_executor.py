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

import signal
import psutil
from src.common.blocking import wait_until_true
from src.driver_io.file.file import File
from src.executors.command_executor import prepare_std_outputs, prepare_printable_command, prepare_executable_command

class ProcessExecutor(object):
    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("ProcessExecutor")
        self.logger_factory = logger_factory
        self.file_ref = File
        self.process = None
        self.KILL_TIMEOUT = 2

    def start(self, command, stdout_path, stderr_path):
        printable_command = prepare_printable_command(command)
        executable_command = prepare_executable_command(command)
        stdout, stderr = prepare_std_outputs(self.file_ref, self.logger_factory, stdout_path, stderr_path)
        self.logger.info("Following process will be started:\n{}".format(printable_command))
        self.process = psutil.Popen(
            executable_command,
            stdout=stdout.open_file(mode="a"),
            stderr=stderr.open_file(mode="a")
        )
        self.logger.info("Process started with pid [{}]".format(self.process.pid))
        return self.process

    def kill(self):
        self.process.send_signal(signal.SIGKILL)
        exit_code = self.process.process.wait(timeout=self.KILL_TIMEOUT)
        return exit_code

    def wait_for_pid(self):
        return wait_until_true(self.is_pid_in_process_list)

    def is_process_running(self):
        if self.process:
            return self.process.is_running()
        return False

    def is_pid_in_process_list(self):
        if self.process:
            return psutil.pid_exists(self.process.pid)
        return False

    def get_opened_file_list(self):
        open_files = self.process.open_files()
        if open_files:
            self.logger.error("Found remaining open files: {}".format(open_files))
        return open_files

    def dump_process_information(self):
        self.logger.info("Process information: [{}]".format(str(self.process.as_dict())))

    def get_process_information(self):
        return self.process.as_dict()
