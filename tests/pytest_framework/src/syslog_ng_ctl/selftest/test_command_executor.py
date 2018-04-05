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

import pytest
from src.syslog_ng_ctl.command_executor import CtlCommandExecutor


@pytest.mark.parametrize("ctl_command_name, expected_ctl_command_args", [
    (
        "stats",
        ["stats"]
    ),
    (
        "stats_reset",
        ["stats", "--reset"]
    ),
    (
        "query_get",
        ["query", "get"]
    ),
    (
        "query_get_sum",
        ["query", "get", "--sum"]
    ),
    (
        "query_reset",
        ["query", "get", "--reset"]
    ),
    (
        "query_list",
        ["query", "list"]
    ),
    (
        "stop",
        ["stop"]
    ),
    (
        "reload",
        ["reload"]
    ),
    (
        "reopen",
        ["reopen"]
    ),
])
def test_slng_ctl_executor(tc_unittest, ctl_command_name, expected_ctl_command_args):
    ctl_command_executor = CtlCommandExecutor(tc_unittest.fake_logger_factory(), tc_unittest.fake_syslog_ng_instance_parameters())
    with pytest.raises(FileNotFoundError):
        ctl_command_executor.slng_ctl_executor(cmd_name=ctl_command_name)
    assert ctl_command_executor.ctl_commands[ctl_command_name]['cmd'] == expected_ctl_command_args
