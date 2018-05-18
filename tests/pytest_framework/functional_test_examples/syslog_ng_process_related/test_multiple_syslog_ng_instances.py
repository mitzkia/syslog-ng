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


def test_multiple_syslog_ng_instances(tc):
    config = tc.new_config(instance_name="server")
    file_source = config.get_file_source({"file_path": "input"})
    file_destination = config.get_file_destination({"file_path": "output"})
    config.create_logpath(sources=[file_source], destinations=[file_destination])

    config_2 = tc.new_config(instance_name="client")
    file_source_2 = config_2.get_file_source({"file_path": "input2"})
    file_destination_2 = config_2.get_file_destination({"file_path": "output2"})
    config_2.create_logpath(sources=[file_source_2], destinations=[file_destination_2])

    syslog_ng = tc.new_syslog_ng(instance_name="server")
    syslog_ng.start(config)

    syslog_ng_2 = tc.new_syslog_ng(instance_name="client")
    syslog_ng_2.start(config_2)
