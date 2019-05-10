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
import logging
import socket
import string
from datetime import datetime

import hypothesis.strategies as st
import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis import Verbosity
from pathlib2 import Path

from src.common.operations import calculate_testcase_name
from src.common.operations import copy_file
from src.syslog_ng.syslog_ng import SyslogNg
from src.syslog_ng.syslog_ng_paths import SyslogNgPaths
from src.syslog_ng_config.syslog_ng_config import SyslogNgConfig
from src.testcase_parameters.testcase_parameters import TestcaseParameters

logger = logging.getLogger(__name__)


input_log = "<38>Feb 11 21:27:22 {} testprogram[9999]: test message\n".format(socket.gethostname())
expected_log = "Feb 11 21:27:22 {} testprogram[9999]: test message\n".format(socket.gethostname())

def create_config(request, testcase_parameters):
    return SyslogNgConfig(testcase_parameters.get_working_dir(), request.getfixturevalue("version"))

def create_syslog_ng(request, testcase_parameters):
    instance_paths = SyslogNgPaths(testcase_parameters).set_syslog_ng_paths("server")
    syslog_ng = SyslogNg(instance_paths, testcase_parameters)
    request.addfinalizer(lambda: syslog_ng.stop())
    return syslog_ng

def property_based_setup(request):
    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    relative_report_dir = str(Path("reports/", current_date))
    testcase_parameters = TestcaseParameters(request, relative_report_dir)
    def prepare_testcase_working_dir(testcase_parameters):
        working_directory = testcase_parameters.get_working_dir()
        if not working_directory.exists():
            working_directory.mkdir(parents=True)
        testcase_file_path = testcase_parameters.get_testcase_file()
        copy_file(testcase_file_path, working_directory)

    def construct_report_file_path(request):
        relative_report_dir = request.config.getoption("--reports")
        testcase_name = calculate_testcase_name(request)
        file_name = "testcase_{}.log".format(testcase_name)
        return str(Path(relative_report_dir, testcase_name, file_name).absolute())

    logging_plugin = request.config.pluginmanager.get_plugin("logging-plugin")
    report_file_path = construct_report_file_path(request)
    logging_plugin.set_log_path(report_file_path)
    request.node.user_properties.append(("report_file_path", report_file_path))
    prepare_testcase_working_dir(testcase_parameters)
    request.addfinalizer(lambda: logger.info("Report file path\n{}\n".format(report_file_path)))
    return testcase_parameters

@settings(max_examples=10)
@given(st.one_of(st.integers(), st.text(min_size=11, alphabet=string.ascii_letters)))
# @given(st.text(min_size=10, alphabet=string.ascii_letters))
def test_persist_name(request, persist_name):
    testcase_parameters = property_based_setup(request)

    config = create_config(request, testcase_parameters)
    syslog_ng = create_syslog_ng(request, testcase_parameters)

    file_source = config.create_file_source(file_name="input.log")
    file_destination = config.create_file_destination(file_name="output.log", persist_name=persist_name)
    config.create_logpath(statements=[file_source, file_destination])

    counter = 1
    file_source.write_log(input_log, counter)
    if isinstance(persist_name, int):
        with pytest.raises(Exception) as execinfo:
            syslog_ng.start(config)
        assert "syslog-ng can not started" in str(execinfo.value)
    elif isinstance(persist_name, str):
        syslog_ng.start(config)
        assert file_destination.read_logs(counter) == [expected_log] * counter
