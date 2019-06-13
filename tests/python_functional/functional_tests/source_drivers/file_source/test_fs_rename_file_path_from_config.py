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
from pathlib2 import Path

import src.testcase_parameters.testcase_parameters as tc_parameters


def test_fs_rename_file_path_from_config(config, syslog_ng, generated_bsd_messages):
    file_source = config.create_file_source(file_name="input.log")
    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[file_source, file_destination])

    input_messages, expected_messages = generated_bsd_messages

    file_source.write_log(input_messages[1], counter=1)
    syslog_ng.start(config)
    assert file_destination.read_log() == expected_messages[1]

    new_input_path = Path(tc_parameters.WORKING_DIR, "input2.log")
    file_source.set_path(str(new_input_path))
    assert not new_input_path.exists()
    file_source.write_log(input_messages[2], counter=1)
    assert new_input_path.exists()
    syslog_ng.reload(config)

    assert file_destination.read_log() == expected_messages[2]
