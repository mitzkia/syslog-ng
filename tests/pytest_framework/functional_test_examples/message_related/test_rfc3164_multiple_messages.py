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

def test_rfc3164_multiple_messages(tc):
    config = tc.new_config()
    config.add_global_options({"stats_level": 3})
    file_source = config.get_file_source({"file_path": "input"})
    file_destination = config.get_file_destination({"file_path": "output"})
    config.create_logpath(sources=[file_source], destinations=[file_destination])

    message_counter = 20
    bsd_messages = tc.new_bsd_message().build(counter=message_counter)
    file_source.write_messages(bsd_messages)

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    output_message = file_destination.read_all_messages()
    expected_output_message = bsd_messages[0].remove_priority().build()
    assert output_message == expected_output_message.get_messages(message_counter)

    fd_counters = file_destination.get_counters()
    assert fd_counters == {
        "processed": message_counter,
        "written": message_counter,
        "queued": 0,
        "dropped": 0,
        "memory_usage": 0
    }
