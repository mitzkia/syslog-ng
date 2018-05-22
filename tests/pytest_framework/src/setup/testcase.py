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

from src.common.path_and_operations import copy_file, construct_path
from src.common.random_id import RandomId
from src.meta.testcase_meta import TestcaseMeta
from src.meta.syslog_ng_meta import SyslogNgMeta
from src.logger.logger_factory import LoggerFactory
from src.syslog_ng_config.syslog_ng_config import SyslogNgConfig
from src.syslog_ng.syslog_ng import SyslogNg
from src.syslog_ng_ctl.syslog_ng_ctl import SyslogNgCtl
from src.message.bsd_message_builder import BSDMessageBuilder
from src.message.ietf_message_builder import IETFMessageBuilder
from src.message.log_message import LogMessage


class SetupTestCase(object):
    def __init__(self, testcase_context):
        self.testcase_context = testcase_context
        self.testcase_meta = TestcaseMeta(testcase_context)
        self.prepare_testcase_working_dir()

        self.logger_factory = LoggerFactory(
            report_file=self.testcase_meta.get_report_file(),
            loglevel=self.testcase_meta.get_loglevel()
        )
        self.logger = self.logger_factory.create_logger("Setup", use_console_handler=True, use_file_handler=True)

        self.teardown_actions = []
        testcase_context.addfinalizer(self.teardown)
        self.logger.info("Testcase setup finish:%s", self.testcase_meta.get_testcase_name())

    def prepare_testcase_working_dir(self):
        working_directory = self.testcase_meta.get_working_dir()
        if not working_directory.exists():
            working_directory.mkdir(parents=True)
        testcase_file_path = self.testcase_meta.get_testcase_file()
        copy_file(testcase_file_path, working_directory)

    def teardown(self):
        self.logger = self.logger_factory.create_logger("Teardown", use_console_handler=True, use_file_handler=True)
        self.logger.info("Testcase teardown start:%s", self.testcase_meta.get_testcase_name())
        for inner_function in self.teardown_actions:
            try:
                inner_function()
            except OSError:
                pass
        self.log_assertion_error()
        self.logger.info("Testcase teardown finish:%s", self.testcase_meta.get_testcase_name())

    def log_assertion_error(self):
        terminalreporter = self.testcase_context.config.pluginmanager.getplugin('terminalreporter')
        if terminalreporter.stats.get('failed'):
            for failed_report in terminalreporter.stats.get('failed'):
                if failed_report.location[2] == self.testcase_context.node.name:
                    self.logger = self.logger_factory.create_logger("Teardown", use_console_handler=False, use_file_handler=True)
                    self.logger.error(str(failed_report.longrepr))

    def new_file_path(self, prefix):
        working_directory = self.testcase_meta.get_working_dir()
        file_name = "{}_{}.log".format(prefix, RandomId(use_static_seed=False).get_unique_id())
        return str(construct_path(working_directory, file_name))

    def new_config(self, instance_name="server"):
        instance_parameters = SyslogNgMeta(self.testcase_context, self.testcase_meta).set_syslog_ng_meta(instance_name)
        syslog_ng = SyslogNg(self.logger_factory, instance_parameters)
        syslog_ng_version = syslog_ng.get_version()
        return SyslogNgConfig(self.logger_factory, instance_parameters, syslog_ng_version)

    def new_syslog_ng(self, instance_name="server"):
        instance_parameters = SyslogNgMeta(self.testcase_context, self.testcase_meta).set_syslog_ng_meta(instance_name)
        syslog_ng = SyslogNg(self.logger_factory, instance_parameters)
        self.teardown_actions.append(syslog_ng.stop)
        return syslog_ng

    def new_syslog_ng_ctl(self, instance_name="server"):
        instance_parameters = SyslogNgMeta(self.testcase_context, self.testcase_meta).set_syslog_ng_meta(instance_name)
        return SyslogNgCtl(self.logger_factory, instance_parameters)

    @staticmethod
    def new_bsd_message(message=None):
        return BSDMessageBuilder(message)

    @staticmethod
    def new_ietf_message(message=None):
        return IETFMessageBuilder(message)

    @staticmethod
    def new_log_message(message=None):
        return LogMessage(message)
