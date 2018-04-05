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
from src.executors.command.executor import CommandExecutor
from src.driver_io.file_based.file import File


@pytest.mark.parametrize("command, expected_stdout, expected_stderr, expected_exit_code, expected_all_output", [
    (
        ["grep", "a", "a"],
        "",
        "grep: a: No such file or directory\n",
        2,
        (2, '', 'grep: a: No such file or directory\n')
    ),
    (
        ["echo", "a"],
        "a\n",
        "",
        0,
        (0, 'a\n', '')
    ),
])
def test_execute_command(tc_unittest, command, expected_stdout, expected_stderr, expected_exit_code, expected_all_output):
    stdout_file = tc_unittest.fake_file_register().get_registered_file_path("stdout")
    stderr_file = tc_unittest.fake_file_register().get_registered_file_path("stderr")
    command_executor = CommandExecutor(tc_unittest.fake_logger_factory(), command, stdout_file, stderr_file)
    assert command_executor.get_stdout() == expected_stdout
    assert command_executor.get_stderr() == expected_stderr
    assert command_executor.get_exit_code() == expected_exit_code
    assert command_executor.get_all() == expected_all_output
    File(tc_unittest.fake_logger_factory(), stdout_file).delete_file()
    File(tc_unittest.fake_logger_factory(), stderr_file).delete_file()
