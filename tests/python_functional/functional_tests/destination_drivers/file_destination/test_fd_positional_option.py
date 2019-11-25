#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2019 Balabit
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
from pathlib2 import Path

import src.testcase_parameters.testcase_parameters as tc_parameters


def test_fd_positional_option_missing(config, syslog_ng):
    # destination destination_24638 { file (); };
    file_source = config.create_file_source()
    file_destination = config.create_file_destination(file_name="skip")
    config.create_logpath(statements=[file_source, file_destination])

    with pytest.raises(Exception) as excinfo:
        syslog_ng.start(config)
    assert "syslog-ng can not started due to config syntax error" in str(excinfo.value)


def test_fd_positional_option_empty(config, syslog_ng):
    # destination destination_24638 { file (""); };
    file_source = config.create_file_source()
    file_destination = config.create_file_destination(file_name='""')
    config.create_logpath(statements=[file_source, file_destination])

    file_source.write_log("dummy message\n")

    syslog_ng.start(config)

    assert syslog_ng.wait_for_console_log(message="Error opening file for writing; filename='', error='No such file or directory (2)'")


def test_fd_positional_option_custom_dir(config, syslog_ng):
    custom_dir = Path(tc_parameters.WORKING_DIR, "custom_dir")
    custom_dir.mkdir()
    file_source = config.create_file_source()
    file_destination = config.create_file_destination(file_name=str(custom_dir))
    config.create_logpath(statements=[file_source, file_destination])

    file_source.write_log("dummy message\n")

    syslog_ng.start(config)

    assert syslog_ng.wait_for_console_log(message="Error opening file for writing")
