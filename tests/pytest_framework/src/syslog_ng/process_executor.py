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
from src.executors.process import ProcessExecutor


class SlngProcessExecutor(object):

    def __init__(self, logger_factory, instance_parameters):
        self.logger_factory = logger_factory
        self.process_executor = ProcessExecutor(logger_factory)
        working_dir = instance_parameters["dir_paths"]["working_dir"]
        syslog_ng_binary_path = instance_parameters["binary_file_paths"]["syslog_ng_binary"]
        config_path = instance_parameters["file_paths"]["config_path"]
        persist_path = instance_parameters["file_paths"]["persist_path"]
        pid_path = instance_parameters["file_paths"]["pid_path"]
        control_socket_path = instance_parameters["file_paths"]["control_socket_path"]
        self.process_start_command_args = {
            "start": {
                "cmd": [
                    syslog_ng_binary_path,
                    "--foreground",
                    "--stderr",
                    "--debug",
                    "--trace",
                    "--verbose",
                    "--startup-debug",
                    "--no-caps",
                    "--enable-core",
                    "--cfgfile={}".format(config_path),
                    "--persist-file={}".format(persist_path),
                    "--pidfile={}".format(pid_path),
                    "--control={}".format(control_socket_path),
                ],
                "stdout": os.path.join(working_dir, "slng_process_stdout"),
                "stderr": os.path.join(working_dir, "slng_process_stderr"),
            },
            "strace": {
                "cmd": ["strace", "-s", "8888", "-ff", "-o", os.path.join(working_dir, "strace.log")],
                "stdout": os.path.join(working_dir, "slng_strace_stdout"),
                "stderr": os.path.join(working_dir, "slng_strace_stderr"),
            },
            "perf": {
                "cmd": [
                    "perf",
                    "record",
                    "-g",
                    "-v",
                    "-s",
                    "-F",
                    "99",
                    "--output={}".format(os.path.join(working_dir, "perf.log")),
                ],
                "stdout": os.path.join(working_dir, "slng_perf_stdout"),
                "stderr": os.path.join(working_dir, "slng_perf_stderr"),
            },
            "valgrind": {
                "cmd": [
                    "valgrind",
                    "--run-libc-freeres=no",
                    "--show-leak-kinds=all",
                    "--track-origins=yes",
                    "--tool=memcheck",
                    "--leak-check=full",
                    "--keep-stacktraces=alloc-and-free",
                    "--read-var-info=yes",
                    "--error-limit=no",
                    "--num-callers=40",
                    "--verbose",
                    "--log-file={}".format(os.path.join(working_dir, "valgrind.log")),
                ],
                "stdout": os.path.join(working_dir, "slng_valgrind_stdout"),
                "stderr": os.path.join(working_dir, "slng_valgrind_stderr"),
            },
        }

    def slng_process_start(self):
        return self.process_executor.start(
            self.process_start_command_args["start"]["cmd"],
            self.process_start_command_args["start"]["stdout"],
            self.process_start_command_args["start"]["stderr"],
        )

    def slng_process_start_behind(self, external_tool):
        concatenated_command = self.process_start_command_args[external_tool]["cmd"] + self.process_start_command_args[
            "start"
        ][
            "cmd"
        ]
        return self.process_executor.start(
            concatenated_command,
            self.process_start_command_args[external_tool]["stdout"],
            self.process_start_command_args[external_tool]["stderr"],
        )

    def slng_process_reload(self):
        return self.process_executor.reload()

    def slng_process_stop(self):
        return self.process_executor.stop()

    def get_process(self):
        return self.process_executor.process_object

    def get_pid(self):
        return self.process_executor.pid

    def slng_is_running(self):
        return self.process_executor.is_process_running()
