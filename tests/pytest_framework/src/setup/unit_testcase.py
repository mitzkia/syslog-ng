#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from mockito import when, unstub
from src.common.path_and_operations import construct_path, open_file
from src.meta.testcase_meta import get_testcase_name
from src.common.random_id import RandomId
from src.logger.logger_factory import LoggerFactory
from src.meta.testcase_meta import TestcaseMeta

class SetupUnitTestcase(object):
    def __init__(self, testcase_context, get_current_date):
        self.testcase_context = testcase_context
        self.get_current_date = get_current_date
        self.registerd_dirs = []
        self.registerd_files = []
        self.registered_file_objects = []

        self.testcase_context.addfinalizer(self.teardown)

    def get_temp_dir(self):
        testcase_name = get_testcase_name(self.testcase_context)
        testcase_subdir = "{}_{}".format(self.get_current_date(), testcase_name)
        temp_dir = construct_path("/tmp", testcase_subdir)
        temp_dir.mkdir()
        self.registerd_dirs.append(temp_dir)
        return temp_dir

    def get_temp_file(self):
        temp_dir = self.get_temp_dir()
        temp_file_path = construct_path(temp_dir, RandomId(use_static_seed=False).get_unique_id())
        self.registerd_files.append(temp_file_path)
        return temp_file_path

    def get_fake_testcase_meta(self):
        when(self.testcase_context).getfixturevalue("installdir").thenReturn(self.get_temp_dir())
        when(self.testcase_context).getfixturevalue("reports").thenReturn(self.get_temp_dir())
        when(self.testcase_context).getfixturevalue("loglevel").thenReturn("info")
        return TestcaseMeta(self.testcase_context)

    def get_fake_logger_factory(self):
        loglevel = self.testcase_context.getfixturevalue("loglevel")
        report_file_path = self.get_temp_file()
        return LoggerFactory(
            report_file_path,
            loglevel,
            use_console_handler=True,
            use_file_handler=False)

    @staticmethod
    def get_utf8_test_messages(counter):
        utf8_test_message = "test message - öüóőúéáű"
        result_content = ""
        for i in range(1, counter+1):
            result_content += "{} - {}\n".format(utf8_test_message, i)
        return result_content

    def prepare_input_file(self, input_content):
        input_file_path = self.get_temp_file()
        file_writer_object = open_file(input_file_path, "a+")
        file_reader_object = open_file(input_file_path, "r")
        self.registered_file_objects.append(file_writer_object)
        self.registered_file_objects.append(file_reader_object)

        file_writer_object.write(input_content)
        file_writer_object.flush()
        return file_writer_object, file_reader_object

    def teardown(self):
        for registered_file_object in self.registered_file_objects:
            registered_file_object.close()

        for temp_file in self.registerd_files:
            if temp_file.exists():
                temp_file.unlink()

        for temp_dir in self.registerd_dirs:
            if temp_dir.exists():
                temp_dir.rmdir()
        unstub()
