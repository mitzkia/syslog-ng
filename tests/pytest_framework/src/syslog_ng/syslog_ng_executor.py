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

from src.common.path_and_operations import construct_path
from src.executors.command_executor import CommandExecutor
from src.executors.process_executor import ProcessExecutor

class SyslogNgExecutor(object):
    def __init__(self, logger_factory, instance_parameters):
        self.instance_parameters = instance_parameters
        self.working_dir = instance_parameters.get_working_dir()
        syslog_ng_binary_path = instance_parameters.get_syslog_ng_bin()
        config_path = instance_parameters.get_config_path()
        persist_path = instance_parameters.get_persist_path()
        pid_path = instance_parameters.get_pid_path()
        control_socket_path = instance_parameters.get_control_socket_path()
        self.processes_and_arguments = {
            "start": [
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
                "--control={}".format(control_socket_path)
            ],
            "strace": [
                "strace",
                "-s",
                "8888",
                "-ff",
                "-o",
                construct_path(self.working_dir, 'strace.log')
            ],
            "perf": [
                "perf",
                "record",
                "-g",
                "--verbose",
                "--stat",
                "--freq=99",
                "--output={}".format(construct_path(self.working_dir, 'perf.log'))
            ],
            "valgrind": [
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
                "--log-file={}".format(construct_path(self.working_dir, 'valgrind.log'))
            ]
        }
        self.commands_and_arguments = {
            "version": [
                syslog_ng_binary_path,
                "--version"
            ],
            "syntax_only": [
                syslog_ng_binary_path,
                "--enable-core",
                "--syntax-only",
                "--cfgfile={}".format(config_path)
            ],
            "preprocess-into": [
                syslog_ng_binary_path,
                "--foreground",
                "--preprocess-into={}".format(construct_path(self.working_dir, 'syslog-ng-preprocessed.conf'))
            ],
            "gdb-bt-full": [
                "gdb",
                "-ex",
                "bt full",
                "--batch",
                syslog_ng_binary_path,
                "--core"
            ]
        }
        self.process_executor = ProcessExecutor(logger_factory)
        self.command_executor = CommandExecutor(logger_factory)

    def run_process(self, process_short_name):
        return self.process_executor.start(
            command=self.processes_and_arguments[process_short_name],
            stdout_path=self.construct_std_file_path(process_short_name, "stdout"),
            stderr_path=self.construct_std_file_path(process_short_name, "stderr"),
        ), self.construct_std_file_path(process_short_name, "stderr")

    def run_process_behind(self, process_short_name):
        concated_command = self.processes_and_arguments[process_short_name] + self.processes_and_arguments['start']
        return self.process_executor.start(
            command=concated_command,
            stdout_path=self.construct_std_file_path(process_short_name, "stdout"),
            stderr_path=self.construct_std_file_path(process_short_name, "stderr"),
        ), self.construct_std_file_path(process_short_name, "stderr")

    def run_command(self, command_short_name, core_file=None):
        if core_file:
            self.commands_and_arguments[command_short_name].append(core_file)
        return self.command_executor.run(
            command=self.commands_and_arguments[command_short_name],
            stdout_path=self.construct_std_file_path(command_short_name, "stdout"),
            stderr_path=self.construct_std_file_path(command_short_name, "stderr")
        )

    def construct_std_file_path(self, command_short_name, std_type):
        instance_name = self.instance_parameters.get_instance_name()
        return construct_path(self.working_dir, "syslog_ng_{}_{}_{}".format(instance_name, command_short_name, std_type))

    def get_process_info(self):
        return self.process_executor.get_process_information()
