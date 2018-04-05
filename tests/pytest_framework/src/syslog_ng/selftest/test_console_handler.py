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
from src.syslog_ng.console_handler import SlngConsoleHandler
from src.common import blocking
blocking.MONITORING_TIME = 0.5


def get_dependencies(tc_unittest):
    slng_console_handler = SlngConsoleHandler(tc_unittest.fake_logger_factory())
    return slng_console_handler, tc_unittest.fake_path()


@pytest.mark.parametrize("console_message, expected_result", [
    (b"syslog-ng starting up;\n", True),
    (b"fake message\n", False),
])
def test_wait_for_start_message(tc_unittest, console_message, expected_result):
    slng_console_handler, fake_path = get_dependencies(tc_unittest)
    fake_path.write(console_message)
    fake_path.seek(0)
    assert slng_console_handler.wait_for_start_message(fake_path.name) is expected_result
    fake_path.close()


@pytest.mark.parametrize("console_message, expected_result", [
    (b"syslog-ng shutting down;\n", True),
    (b"fake message\n", False),
])
def test_wait_for_stop_message(tc_unittest, console_message, expected_result):
    slng_console_handler, fake_path = get_dependencies(tc_unittest)
    fake_path.write(console_message)
    fake_path.seek(0)
    assert slng_console_handler.wait_for_stop_message(fake_path.name) is expected_result
    fake_path.close()


@pytest.mark.parametrize("console_message, expected_result", [
    (b"New configuration initialized\n"
     b"Configuration reload request received, reloading configuration\n"
     b"Configuration reload finished\n", True),
    (b"fake message\n", False),
])
def test_wait_for_reload_message(tc_unittest, console_message, expected_result):
    slng_console_handler, fake_path = get_dependencies(tc_unittest)
    fake_path.write(console_message)
    fake_path.seek(0)
    assert slng_console_handler.wait_for_reload_message(fake_path.name) is expected_result
    fake_path.close()
