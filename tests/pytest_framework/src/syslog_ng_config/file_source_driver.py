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

from src.syslog_ng_config.source_driver import SourceDriver
from src.driver_io.file_based.file_interface import FileInterface

class FileSourceDriver(SourceDriver):
    def __init__(self, logger_factory, instance_parameters, config_tree):
        self.config_tree = config_tree
        driver_io = FileInterface(logger_factory)
        super().__init__(logger_factory, instance_parameters, self.config_tree, driver_io)
        self.working_dir = instance_parameters["dir_paths"]["working_dir"]

    def configure_options(self, options):
        self.set_file_path_mandatory_option(options, "file_path", "file_source", self.working_dir)
        self.add_options(options)
