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
import sys
from colorlog import ColoredFormatter


class Logger(logging.Logger):
    def __init__(self, logger_name, report_file, loglevel, use_console_handler=True, use_file_handler=True):
        super().__init__(logger_name, loglevel)
        self.handlers = []
        if use_console_handler:
            self.__set_consolehandler()
        if use_file_handler:
            self.__set_filehandler(file_name=report_file)

    def __set_filehandler(self, file_name=None):
        file_handler = logging.FileHandler(file_name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def __set_consolehandler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        logging.captureWarnings(capture=True)
        formatter = ColoredFormatter(
            "\n%(log_color)s%(asctime)s - %(name)s - %(levelname)-5s%(reset)s- %(message_log_color)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={
                'message': {
                    'ERROR': 'red',
                    'CRITICAL': 'red'
                }
            },
            style='%'
        )
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

    def write_message_based_on_value(self, message, value, loglevel=logging.DEBUG):
        pred = value
        message = "{}: [{}]".format(message, pred)
        if pred:
            self.log(loglevel, message)
        else:
            self.error(message)
