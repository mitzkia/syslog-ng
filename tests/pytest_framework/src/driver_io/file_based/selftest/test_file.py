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
from src.driver_io.file_based.file import File


def get_test_message():
    return """new message 1
new message 2"""


def instantiate_file_object_with_content(tc_unittest, file_content=None):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.fake_logger_factory(), temp_file)
    if file_content is None:
        file_content = get_test_message()
    file_object.write(file_content, open_mode="a", normalize_line_endings=False)
    return file_object


def test_read(tc_unittest):
    file_object = instantiate_file_object_with_content(tc_unittest)
    assert file_object.read() == get_test_message()
    file_object.delete_file()


@pytest.mark.parametrize(
    "file_content, expected_result_lines",
    [("test content\n", 1), ("test content\ntest content\n", 2), ("test content\ntest content", 1), ("", 0)],
)
def test_get_number_of_lines(tc_unittest, file_content, expected_result_lines):
    file_object = instantiate_file_object_with_content(tc_unittest, file_content)
    assert file_object.get_number_of_lines() == expected_result_lines
    file_object.delete_file()


def test_is_file_exist(tc_unittest):
    file_object = instantiate_file_object_with_content(tc_unittest)
    assert file_object.is_file_exist() is True
    file_object.delete_file()


def test_is_regular_file(tc_unittest):
    file_object = instantiate_file_object_with_content(tc_unittest)
    assert file_object.is_regular_file() is True
    file_object.delete_file()


def test_get_size(tc_unittest):
    file_object = instantiate_file_object_with_content(tc_unittest)
    assert file_object.get_size() == len(get_test_message())
    file_object.delete_file()


@pytest.mark.parametrize(
    "input_content, read_content",
    [
        ("new message 1\nnew message 2\n", "new message 1\nnew message 2\n"),
        ("new message 1\nnew message 2", "new message 1\nnew message 2\n"),
    ],
)
def test_write_content_normalize_endings_true(tc_unittest, input_content, read_content):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.fake_logger_factory(), temp_file)
    file_object.write(input_content, open_mode="a", normalize_line_endings=True)
    assert file_object.read() == read_content
    file_object.delete_file()


@pytest.mark.parametrize(
    "input_content, read_content",
    [
        ("new message 1\nnew message 2\n", "new message 1\nnew message 2\n"),
        ("new message 1\nnew message 2", "new message 1\nnew message 2"),
    ],
)
def test_write_content_normalize_endings_false(tc_unittest, input_content, read_content):
    temp_file = tc_unittest.fake_file_register().get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.fake_logger_factory(), temp_file)
    file_object.write(input_content, open_mode="a", normalize_line_endings=False)
    assert file_object.read() == read_content
    file_object.delete_file()
