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

def test_one_statement_one_driver(tc):
    config = tc.new_config()
    config.add_global_options({"stats_level": 3})
    file_source = config.get_file_source({"file_path": "input"})
    file_destination = config.get_file_destination({"file_path": "output"})
    config.create_logpath(sources=[file_source], destinations=[file_destination], flags="flow-control")

    ######
    message_counter_1 = 1

    bsd_message = tc.new_bsd_message().program("random_program1").build()
    file_source.write_message(bsd_message)

    syslog_ng = tc.new_syslog_ng()
    syslog_ng.start(config)

    output_message = file_destination.read_message()
    expected_output_message = bsd_message.remove_priority().build()
    assert output_message == expected_output_message.get_message()

    ######
    message_counter_2 = 101

    bsd_messages = tc.new_bsd_message().program("random_program2").build(message_counter_2)
    file_source.write_messages(bsd_messages)

    output_messages = file_destination.read_messages(message_counter_2)
    expected_output_message = bsd_messages[0].remove_priority().build()
    assert output_messages == expected_output_message.get_messages(message_counter_2)

    ######
    message_counter_3 = 19

    for i in range(0, message_counter_3):
        bsd_message = tc.new_bsd_message().program("random_program_{}".format(i)).build(1)
        file_source.write_message(bsd_message)
        syslog_ng.reload()
        output_message = file_destination.read_message()
        expected_output_message = bsd_message.remove_priority().build()

        assert output_message == expected_output_message.get_message()

    ######
    ctl_counters = file_destination.get_counters()

    assert ctl_counters == {
        "processed": message_counter_1 + message_counter_2 + message_counter_3,
        "written": message_counter_1 + message_counter_2 + message_counter_3,
        "queued": 0,
        "dropped": 0,
        "memory_usage": 0
    }
    print(syslog_ng.get_process_info())
