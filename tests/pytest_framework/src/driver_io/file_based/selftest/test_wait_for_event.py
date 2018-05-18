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
from src.driver_io.file_based.wait_for_event import FileWaitForEvent
from src.driver_io.file_based.file import File
from src.common import blocking

blocking.MONITORING_TIME = 0.5


def test_wait_for_creation_file_created_with_content(tc_unittest):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.fake_logger_factory(), temp_file)
    file_manager = FileWaitForEvent(tc_unittest.fake_logger_factory(), temp_file)
    file_object.write("new message 1\n", open_mode="a+", normalize_line_endings=True)

    assert file_manager.wait_for_creation() is True
    file_object.delete_file()


def test_wait_for_creation_file_created_with_empty_content(tc_unittest):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.fake_logger_factory(), temp_file)
    file_manager = FileWaitForEvent(tc_unittest.fake_logger_factory(), temp_file)
    file_object.write("", open_mode="a+", normalize_line_endings=False)

    assert file_manager.wait_for_creation() is False
    file_object.delete_file()


def test_wait_for_creation_file_not_created(tc_unittest):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_manager = FileWaitForEvent(tc_unittest.fake_logger_factory(), temp_file)

    with pytest.raises(FileNotFoundError):
        file_manager.wait_for_creation()


# @pytest.mark.parametrize("file_content, expected_lines, expected_result", [
#     (
#         "new message 1\nnew message 2\nnew message 3\n",
#         3,
#         True
#     ),
#     (
#         "new message 1\nnew message 2\nnew message 3\n",
#         4,
#         False
#     ),
#     (
#         "new message 1\nnew message 2\nnew message 3\n",
#         1,
#         False
#     ),
# ])
# def test_wait_for_number_of_lines(tc_unittest, file_content, expected_lines, expected_result):
#     temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
#     file_object = File(tc_unittest.fake_logger_factory(), temp_file)
#     file_manager = FileWaitForEvent(tc_unittest.fake_logger_factory(), temp_file)
#     file_object.write(file_content, open_mode="a+", normalize_line_endings=True)

#     assert file_manager.wait_for_number_of_lines(expected_lines) == expected_result
#     file_object.delete_file()


@pytest.mark.parametrize(
    "file_content, expected_content, expected_result",
    [
        ("new message 1\nnew message 2\nnew message 3\n", "new message 2\n", True),
        ("new message 1\nnew message 2\nnew message 3\n", "not arrived message\n", False),
    ],
)
def test_wait_for_message(tc_unittest, file_content, expected_content, expected_result):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.fake_logger_factory(), temp_file)
    file_wait_for_event = FileWaitForEvent(tc_unittest.fake_logger_factory(), temp_file)

    file_object.write(file_content, open_mode="a+", normalize_line_endings=True)
    assert file_wait_for_event.wait_for_message(expected_content) is expected_result
    file_object.delete_file()


def test_wait_for_message_file_not_created(tc_unittest):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_wait_for_event = FileWaitForEvent(tc_unittest.fake_logger_factory(), temp_file)
    with pytest.raises(FileNotFoundError):
        assert file_wait_for_event.wait_for_message("not arrived message\n")
