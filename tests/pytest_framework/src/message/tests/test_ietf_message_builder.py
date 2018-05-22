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

from src.message.ietf_message_builder import IETFMessageBuilder

def test_ietf_message_builder_default_message():
    ietf_message = IETFMessageBuilder("message").build()
    assert ietf_message.get_raw_message() == '<38>1 2017-06-01T08:05:04+02:00 tristram testprogram 9999 - [meta sequenceId="1"] message\n'

def test_ietf_message_builder_all_parts_counter_3():
    ietf_messages = IETFMessageBuilder("test message").priority("11").syslog_protocol_version("2").iso_timestamp("2003-12-31T22:14:15.003Z").hostname("myhost").program("myprogram").pid("1111").message_id("msg_id").sdata("custom-sdata").message("test message 2").build(counter=3)
    for ietf_message in ietf_messages:
        assert ietf_message.get_raw_message() == "<11>2 2003-12-31T22:14:15.003Z myhost myprogram 1111 msg_id custom-sdata test message 2\n"
    assert len(ietf_messages) == 3
