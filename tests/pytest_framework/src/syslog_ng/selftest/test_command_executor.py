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
from src.syslog_ng.command_executor import SlngCommandExecutor


class FakePopen(object):

    def __init__(self, args, stderr, stdout):
        self.pid = 1234

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def __enter__(self):
        return True

    def wait(self, timeout):
        return True


def patch_dependencies():
    patch(psutil.Popen, FakePopen)


def get_dependencies(tc_unittest):
    return SlngCommandExecutor(tc_unittest.fake_logger_factory(), tc_unittest.fake_syslog_ng_instance_parameters())


@pytest.mark.parametrize("cmd_reference", ["version", "syntax_only", "gdb_bt_full"])
def test_slng_executor(tc_unittest, cmd_reference):
    patch_dependencies()
    slng_command_executor = get_dependencies(tc_unittest)
    slng_command_executor.slng_executor(cmd_reference)
    unstub()
