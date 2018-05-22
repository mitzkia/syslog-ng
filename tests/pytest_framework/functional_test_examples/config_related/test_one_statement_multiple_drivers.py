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

def test_one_statement_multiple_drivers(tc):
    config = tc.new_config()
    config.add_global_options({"stats_level": 3})

    file_source = config.get_file_source({"file_path": "input"})
    file_destination = config.get_file_destination({"file_path": "output"})
    file_destination2 = config.get_file_destination({"file_path": "output2"}, build=False)

    file_destination2.register_driver(parent_stmt_node=file_destination.get_statement())
    config.create_logpath(sources=[file_source], destinations=[file_destination])

    bsd_message = tc.new_bsd_message().program("random_program1").build()
    file_source.write_message(bsd_message)

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    output_message1 = file_destination.read_message()
    output_message2 = file_destination2.read_message()

    expected_output_message = bsd_message.remove_priority().build()

    assert output_message1 == output_message2 == expected_output_message.get_message()
