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
from src.logger.logger_factory import LoggerFactory

def test_logger_file_handler():
    file_path = "/tmp/unittestcase.log"
    logger_factory = LoggerFactory(
        report_file_path=file_path,
        loglevel="debug",
        use_console_handler=False,
        use_file_handler=True)
    logger_name = "UnitTest"
    test_message = "test message"
    logger = logger_factory.create_logger(logger_name)
    logger.info(test_message)
    logger.debug(test_message)
    logger.error(test_message)

    with open(file_path, 'r') as file_object:
        file_content = file_object.read()
    assert "- {} - INFO - {}\n".format(logger_name, test_message) in file_content
    assert "- {} - DEBUG - {}\n".format(logger_name, test_message) in file_content
    assert "- {} - ERROR - {}\n".format(logger_name, test_message) in file_content
    assert file_content.count("\n") == 3

    os.unlink(file_path)

def test_logger_file_handler_is_disabled():
    file_path = "/tmp/unittestcase.log"
    logger_factory = LoggerFactory(
        report_file_path=file_path,
        loglevel="debug",
        use_console_handler=False,
        use_file_handler=False)
    logger_name = "UnitTest"
    test_message = "test message"
    logger = logger_factory.create_logger(logger_name)
    logger.info(test_message)
    logger.debug(test_message)
    logger.error(test_message)

    assert os.path.exists(file_path) is False

def test_logger_write_message_based_on_value():
    file_path = "/tmp/unittestcase.log"
    logger_factory = LoggerFactory(
        report_file_path=file_path,
        loglevel="debug",
        use_console_handler=False,
        use_file_handler=True)
    logger_name = "UnitTest"
    test_message = "test message"
    logger = logger_factory.create_logger(logger_name)
    logger.write_message_based_on_value(test_message, True)
    logger.write_message_based_on_value(test_message, False)

    with open(file_path, 'r') as file_object:
        file_content = file_object.read()
    assert "- {} - DEBUG - {}: [True]\n".format(logger_name, test_message) in file_content
    assert "- {} - ERROR - {}: [False]\n".format(logger_name, test_message) in file_content
    assert file_content.count("\n") == 2

    os.unlink(file_path)
