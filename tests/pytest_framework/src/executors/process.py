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


class ProcessExecutor(object):

    def __init__(self, logger_factory):
        self.logger = logger_factory.create_logger("ProcessExecutor")
        self.command_of_process = None
        self.process_object = None
        self.pid = None
        self.exit_code = None

    def start(self, command_of_process, stdout, stderr):
        self.command_of_process = command_of_process
        self.logger.info("Following process will be started: [{}]".format(" ".join(command_of_process)))
        with open(stdout, "a") as stdout_fd, open(stderr, "a") as stderr_fd:
            self.process_object = psutil.Popen(command_of_process, stderr=stderr_fd, stdout=stdout_fd)
            self.pid = self.process_object.pid
            self.logger.info("Process started with pid [{}]".format(self.pid))
            return self.process_object

    def stop(self):
        if not self.is_process_running():
            raise Exception("process is not running: [{}]".format(self.process_object))
        try:
            for child_process in self.process_object.children(recursive=True):
                child_process.send_signal(signal.SIGTERM)
            self.process_object.send_signal(signal.SIGTERM)
            self.exit_code = self.process_object.wait(timeout=2)

            if self.exit_code in [0]:
                self.logger.info("Process [{}] stopped gracefully with exit code [{}]".format(self.pid, self.exit_code))
            else:
                self.logger.error(
                    "Process [{}] stopped with crash with exit code [{}]".format(self.pid, self.exit_code)
                )

            self.process_object = None
            self.pid = None
        except psutil.TimeoutExpired:
            self.process_object.send_signal(signal.SIGSEGV)
            raise Exception("Process can not stopped gracefully")

    def reload(self):
        if not self.is_process_running():
            raise Exception("process is not running: [{}]".format(self.process_object))
        try:
            for child_process in self.process_object.children(recursive=True):
                child_process.send_signal(signal.SIGHUP)
            self.process_object.send_signal(signal.SIGHUP)

            self.logger.info("SIGHUP signal sent to process [{}]".format(self.pid))
        except psutil.TimeoutExpired:
            self.process_object.send_signal(signal.SIGSEGV)
            raise Exception("Process can not reloaded gracefully")

    def kill(self):
        self.process_object.send_signal(signal.SIGKILL)
        exit_code = self.process_object.process.wait(timeout=2)
        return exit_code

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

    def get_process(self):
        return self.process_object

    def get_pid(self):
        return self.pid

    def get_exit_code(self):
        return self.exit_code
