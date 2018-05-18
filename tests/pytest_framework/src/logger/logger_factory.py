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
from src.logger.logger import Logger


class LoggerFactory(object):

    def __init__(self, report_file_path, loglevel, use_console_handler=True, use_file_handler=True):
        self.report_file = report_file_path
        self.use_console_handler = use_console_handler
        self.use_file_handler = use_file_handler
        self.string_to_loglevel = {"info": logging.INFO, "debug": logging.DEBUG, "error": logging.ERROR}
        try:
            self.log_level = self.string_to_loglevel[loglevel]
        except KeyError:
            raise Exception("Unknown defined loglevel: [{}]".format(loglevel))

    def create_logger(self, logger_name, use_console_handler=None, use_file_handler=None):
        if not use_console_handler:
            use_console_handler = self.use_console_handler
        if not use_file_handler:
            use_file_handler = self.use_file_handler
        return Logger(
            logger_name,
            self.report_file,
            self.log_level,
            use_console_handler=use_console_handler,
            use_file_handler=use_file_handler,
        )
