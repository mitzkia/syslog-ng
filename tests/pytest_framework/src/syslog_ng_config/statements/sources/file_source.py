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

from src.driver_io.file.file_io import FileIO
from src.syslog_ng_config.statements.sources.source_driver import SourceDriver

class FileSource(SourceDriver):
    def __init__(self, syslog_ng_config, logger_factory, instance_parameters, build_status, options):
        # start inheritance
        empty_driver_content = {
            "driver_name": "file",
            "mandatory_option_name": "file_path",
            "driver_options": {},
            "statement_short_name": "src"
        }
        self.file_io_ref = FileIO
        super(FileSource, self).__init__(logger_factory, instance_parameters, self.file_io_ref, empty_driver_content)
        # set mandatory_options
        self.working_dir = instance_parameters.get_working_dir()
        options = self.set_file_path_mandatory_option(options, "file_source", self.working_dir)
        # build statement
        self.build_statement(build_status, syslog_ng_config, "sources", options)

    def update_options(self, options):
        options = self.update_file_path_mandatory_option(options, "file_source", self.working_dir)
        self.register_options(options)
