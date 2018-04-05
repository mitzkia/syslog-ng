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
from src.driver_io.file_based.interface import FileInterface
from src.driver_io.file_based.file import File
from src.common import blocking
blocking.MONITORING_TIME = 0.5

def get_test_message():
    return """new message 1
new message 2"""

def test_read_write_content_append_mode_normalized_endings(tc_unittest):
    file_interface = FileInterface(tc_unittest.fake_logger_factory())
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_interface.write_content(temp_file, get_test_message(), open_mode="a+", normalize_line_endings=True)
    file_interface.write_content(temp_file, get_test_message(), open_mode="a+", normalize_line_endings=True)
    assert file_interface.read_content(temp_file, expected_message_counter=4) == get_test_message() + "\n" + get_test_message() + "\n"
    File(tc_unittest.fake_logger_factory(), temp_file).delete_file()

def test_read_write_content_file_never_written(tc_unittest):
    file_interface = FileInterface(tc_unittest.fake_logger_factory())
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    with pytest.raises(FileNotFoundError):
        file_interface.read_content(temp_file, expected_message_counter=1)

def test_read_write_empty_content(tc_unittest):
    file_interface = FileInterface(tc_unittest.fake_logger_factory())
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_interface.write_content(temp_file, "", open_mode="a+", normalize_line_endings=False)
    assert file_interface.read_content(temp_file, expected_message_counter=0) == ""
    File(tc_unittest.fake_logger_factory(), temp_file).delete_file()

def test_read_write_content_wait_for_more_message_than_written(tc_unittest):
    # In this case we expect that, we can read only as many messages was sended
    # The fw. will notify the user about if the expected not equals with the actual message counter
    # In real testcases there will be an assert in the testcase about the message counter check
    file_interface = FileInterface(tc_unittest.fake_logger_factory())
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_interface.write_content(temp_file, get_test_message(), open_mode="a+", normalize_line_endings=True)
    assert file_interface.read_content(temp_file, expected_message_counter=4) == get_test_message() + "\n"
    File(tc_unittest.fake_logger_factory(), temp_file).delete_file()

def test_read_write_content_wait_for_less_message_than_written(tc_unittest):
    # In this case we expect that, we can read only as many messages was sended
    # The fw. will notify the user about if the expected not equals with the actual message counter
    # In real testcases there will be an assert in the testcase about the message counter check
    file_interface = FileInterface(tc_unittest.fake_logger_factory())
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_interface.write_content(temp_file, get_test_message(), open_mode="a+", normalize_line_endings=True)
    assert file_interface.read_content(temp_file, expected_message_counter=1) == get_test_message() + "\n"
    File(tc_unittest.fake_logger_factory(), temp_file).delete_file()
