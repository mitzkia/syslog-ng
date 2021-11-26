#!/usr/bin/env python
#############################################################################
# Copyright (c) 2021 One Identity
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
import math
import time

from src.common.file import File
from src.message_builder.log_message import LogMessage
from src.syslog_ng_config.statements.filters.filter import Throttle


KEY_RESOLUTIONS = 5
THROTTLE_RATE = 100

NUM_MSG = 10000
INCOMING_EPS = 1000

TOLERANCE = 0.1


def create_throttled_logpath(config, port_allocator, throttle_rate):
    port = port_allocator()

    s_network = config.create_network_source(port=port, transport="tcp")
    f_throttle = Throttle(template="'$PROGRAM'", rate=throttle_rate)
    d_file = config.create_file_destination(file_name="output_{}.log".format(port))

    config.create_logpath(statements=[s_network, f_throttle, d_file])

    return (s_network, f_throttle, d_file)


def generate_input_messages(key_resolutions, num_msg, formatter):
    input_messages = ""

    for i in range(num_msg):
        program_idx = i % key_resolutions
        log_message = LogMessage().program("test_program_{}".format(program_idx))
        input_messages += formatter.format_message(log_message, add_new_line=True)

    return input_messages


def start_sending_logs(network_sources, num_msg, key_resolutions, eps, formatter):
    input_messages = generate_input_messages(key_resolutions, num_msg, formatter)

    for s_network in network_sources:
        s_network.write_log(input_messages, rate=eps)


def wait_for_constant_msg_flow():
    time.sleep(1)


def is_outgoing_eps_throttled(throttle_filters, throttle_rate, key_resolutions, tolerance):
    measurement_duration = 1  # seconds
    expected_rate = throttle_rate * key_resolutions
    start_msg_counts = []

    for f_throttle in throttle_filters:
        msg_count = f_throttle.get_stats()["matched"]
        start_msg_counts.append(msg_count)

    time.sleep(measurement_duration)

    for i, f_throttle in enumerate(throttle_filters):
        msg_count = f_throttle.get_stats()["matched"]
        outgoing_rate = (msg_count - start_msg_counts[i]) / measurement_duration

        if not math.isclose(outgoing_rate, expected_rate, rel_tol=tolerance):
            raise Exception(
                "Outgoing EPS differs too much from the expected EPS. "
                "outgoing_rate: {}, expected_rate: {}".format(outgoing_rate, expected_rate),
            )

    return True


def count_message_in_file(file_path, message_substring):
    count = 0

    f = File(file_path)
    f.open("r")

    while True:
        msg = f.readline()

        if len(msg) == 0:
            return count

        if message_substring in msg:
            count += 1


def are_messages_received_from_all_key_resolutions(file_destinations, key_resolutions, tolerance):
    for d_file in file_destinations:
        msg_counts = {}

        for program_idx in range(key_resolutions):
            program_field = "test_program_{}".format(program_idx)
            msg_count = count_message_in_file(d_file.get_path(), program_field)
            msg_counts[program_field] = msg_count

        least_messages = min(msg_counts.items(), key=lambda k: k[1])
        most_messages = max(msg_counts.items(), key=lambda k: k[1])
        if not math.isclose(least_messages[1], most_messages[1], rel_tol=tolerance):
            raise Exception(
                "Message counts have too large difference. "
                "least_messages: {}, most_messages: {}".format(least_messages, most_messages),
            )

    return True


def test_throttle_filter(config, syslog_ng, port_allocator, bsd_formatter):
    config.update_global_options(stats_level=1)

    s_network_1, f_throttle_1, d_file_1 = create_throttled_logpath(config, port_allocator, THROTTLE_RATE)
    s_network_2, f_throttle_2, d_file_2 = create_throttled_logpath(config, port_allocator, THROTTLE_RATE)

    syslog_ng.start(config)

    start_sending_logs([s_network_1, s_network_2], NUM_MSG, KEY_RESOLUTIONS, INCOMING_EPS, bsd_formatter)
    wait_for_constant_msg_flow()

    assert is_outgoing_eps_throttled([f_throttle_1, f_throttle_2], THROTTLE_RATE, KEY_RESOLUTIONS, TOLERANCE)

    syslog_ng.stop()

    assert are_messages_received_from_all_key_resolutions([d_file_1, d_file_2], KEY_RESOLUTIONS, TOLERANCE)
