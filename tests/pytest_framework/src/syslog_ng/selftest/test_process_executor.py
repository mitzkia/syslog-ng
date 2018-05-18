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
import pytest
from mockito import patch, unstub
from src.syslog_ng.process_executor import SlngProcessExecutor


class FakePopen(object):

    def __init__(self, args, stderr, stdout):
        self.pid = 1234


def patch_dependencies():
    patch(psutil.Popen, FakePopen)


def get_dependencies(tc_unittest):
    return SlngProcessExecutor(tc_unittest.fake_logger_factory(), tc_unittest.fake_syslog_ng_instance_parameters())


@pytest.mark.parametrize("parent_command_name", ["strace", "perf", "valgrind"])
def test_slng_process_start_behind(tc_unittest, parent_command_name):
    patch_dependencies()
    slng_process_executor = get_dependencies(tc_unittest)
    slng_process_executor.slng_process_start_behind(external_tool=parent_command_name)
    assert parent_command_name in slng_process_executor.process_executor.command_of_process
    assert "--enable-core" in slng_process_executor.process_executor.command_of_process
    unstub()


def test_slng_start_process(tc_unittest):
    patch_dependencies()
    slng_process_executor = get_dependencies(tc_unittest)
    slng_process_executor.slng_process_start()
    assert (
        [
            "{}/sbin/syslog-ng".format(tc_unittest.temp_install_dir),
            "--foreground",
            "--stderr",
            "--debug",
            "--trace",
            "--verbose",
            "--startup-debug",
            "--no-caps",
            "--enable-core",
            "--cfgfile={}/test_slng_start_process/syslog_ng_server.conf".format(tc_unittest.temp_report_dir),
            "--persist-file={}/test_slng_start_process/syslog_ng_server.persist".format(tc_unittest.temp_report_dir),
            "--pidfile={}/test_slng_start_process/syslog_ng_server.pid".format(tc_unittest.temp_report_dir),
            "--control={}/test_slng_start_process/syslog_ng_server.ctl".format(tc_unittest.temp_report_dir),
        ]
        == slng_process_executor.process_executor.command_of_process
    )
    unstub()
