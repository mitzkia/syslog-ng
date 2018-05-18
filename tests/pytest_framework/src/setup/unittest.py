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

import os
import shutil
import tempfile
from mockito import when, unstub
from src.parameters.test_case import TestCaseParameters
from src.parameters.syslog_ng import SyslogNgParameters
from src.logger.logger_factory import LoggerFactory
from src.registers.file import FileRegister


class SetupUnitTestCase(object):

    def __init__(self, testcase_context):
        self.testcase_context = testcase_context

        self.temp_current_dir = tempfile.TemporaryDirectory().name
        when(os).getcwd().thenReturn(self.temp_current_dir)

        self.temp_report_dir = tempfile.TemporaryDirectory().name
        when(self.testcase_context).getfixturevalue("reports").thenReturn(self.temp_report_dir)

        self.temp_install_dir = tempfile.TemporaryDirectory().name
        when(self.testcase_context).getfixturevalue("installdir").thenReturn(self.temp_install_dir)

        when(self.testcase_context).getfixturevalue("loglevel").thenReturn("info")
        self.temp_dir = None
        self.testcase_context.addfinalizer(self.teardown)

    def fake_testcase_parameters(self):
        return TestCaseParameters(self.testcase_context)

    def fake_syslog_ng_parameters(self):
        slng_parameters = SyslogNgParameters(self.testcase_context, self.fake_testcase_parameters())
        self.prepare_testcase_working_dir(self.fake_testcase_parameters()["dir_paths"]["working_dir"])
        return slng_parameters

    def fake_syslog_ng_instance_parameters(self, instance_name="server"):
        return self.fake_syslog_ng_parameters().set_instance_parameters(instance_name)

    @staticmethod
    def fake_logger_factory():
        return LoggerFactory(
            report_file_path=tempfile.TemporaryFile().name,
            loglevel="info",
            use_console_handler=True,
            use_file_handler=False,
        )

    def fake_file_register(self):
        self.temp_dir = tempfile.TemporaryDirectory().name
        file_register = FileRegister(self.fake_logger_factory(), self.temp_dir)
        self.prepare_testcase_working_dir(self.temp_dir)
        return file_register

    @staticmethod
    def fake_path():
        return tempfile.NamedTemporaryFile(delete=True)

    def teardown(self):
        for temp_dir in [self.temp_install_dir, self.temp_report_dir, self.temp_current_dir, self.temp_dir]:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        unstub()

    @staticmethod
    def prepare_testcase_working_dir(working_directory):
        if not os.path.exists(working_directory):
            os.makedirs(working_directory)
