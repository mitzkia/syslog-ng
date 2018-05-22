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

class SyslogNgMeta(object):
    def __init__(self, testcase_context, testcase_meta):
        self.testcase_context = testcase_context
        self.testcase_meta = testcase_meta
        self.instance_name = None
        self.syslog_ng_meta = {}

    def set_syslog_ng_meta(self, instance_name):
        if self.instance_name is not None:
            raise Exception("Instance already configured")
        self.instance_name = instance_name
        working_dir = self.testcase_meta.get_working_dir()
        relative_working_dir = self.testcase_meta.get_relative_working_dir()
        install_dir = self.testcase_context.getfixturevalue("installdir")
        if not install_dir:
            raise ValueError("Missing --installdir start parameter")

        self.syslog_ng_meta[instance_name] = {
            "dirs": {
                "working_dir": working_dir,
                "install_dir": construct_path(install_dir),
            },
            "file_paths": {
                "config_path": construct_path(working_dir, 'syslog_ng_{}.conf'.format(instance_name)),
                "persist_path": construct_path(working_dir, 'syslog_ng_{}.persist'.format(instance_name)),
                "pid_path": construct_path(working_dir, 'syslog_ng_{}.pid'.format(instance_name)),
                "control_socket_path": construct_path(relative_working_dir, 'syslog_ng_{}.ctl'.format(instance_name)),
            },
            "binary_file_paths": {
                "syslog_ng_binary": construct_path(install_dir, "sbin", "syslog-ng"),
                "syslog_ng_ctl": construct_path(install_dir, "sbin", "syslog-ng-ctl"),
            },
        }
        return self

    def get_instance_name(self):
        return self.instance_name

    def get_working_dir(self):
        return self.syslog_ng_meta[self.instance_name]["dirs"]["working_dir"]

    def get_install_dir(self):
        return self.syslog_ng_meta[self.instance_name]["dirs"]["install_dir"]

    def get_config_path(self):
        return self.syslog_ng_meta[self.instance_name]["file_paths"]["config_path"]

    def get_persist_path(self):
        return self.syslog_ng_meta[self.instance_name]["file_paths"]["persist_path"]

    def get_pid_path(self):
        return self.syslog_ng_meta[self.instance_name]["file_paths"]["pid_path"]

    def get_control_socket_path(self):
        return self.syslog_ng_meta[self.instance_name]["file_paths"]["control_socket_path"]

    def get_syslog_ng_bin(self):
        return self.syslog_ng_meta[self.instance_name]["binary_file_paths"]["syslog_ng_binary"]

    def get_syslog_ng_ctl_bin(self):
        return self.syslog_ng_meta[self.instance_name]["binary_file_paths"]["syslog_ng_ctl"]
