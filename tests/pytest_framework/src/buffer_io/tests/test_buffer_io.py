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

from src.buffer_io.buffer_io import BufferIO

def test_buffering(tc_unittest):
    buffer_io = BufferIO(tc_unittest.get_fake_logger_factory())

    input_content = "test message 1\n"
    file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)

    buffer_io.buffering(file_reader_object.read)
    assert input_content == buffer_io.saved_buffer

    input_content2 = "test message 2\n"
    file_writer_object.write(input_content2)
    file_writer_object.flush()
    buffer_io.buffering(file_reader_object.read)
    assert input_content + input_content2 == buffer_io.saved_buffer

def test_buffering_and_eof(tc_unittest):
    buffer_io = BufferIO(tc_unittest.get_fake_logger_factory())

    input_content = "test message\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)
    buffer_io.buffering(file_reader_object.read)
    assert buffer_io.eof is False
    buffer_io.buffering(file_reader_object.read)
    assert buffer_io.eof is True

def test_delete_chars_from_beginning_buffer(tc_unittest):
    buffer_io = BufferIO(tc_unittest.get_fake_logger_factory())

    input_content = "test message\n"
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)
    buffer_io.buffering(file_reader_object.read)
    buffer_io.delete_chars_from_beginning_buffer(last_char_index=4)
    assert buffer_io.saved_buffer == " message\n"

def test_buffering_empty_content(tc_unittest):
    buffer_io = BufferIO(tc_unittest.get_fake_logger_factory())

    input_content = ""
    __file_writer_object, file_reader_object = tc_unittest.prepare_input_file(input_content)

    buffer_io.buffering(file_reader_object.read)
    assert input_content == buffer_io.saved_buffer
