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

from src.message.bsd_message_builder import BSDMessageBuilder

def test_bsd_message_builder_default_message():
    bsd_message = BSDMessageBuilder("message").build()
    assert bsd_message.get_raw_message() == "<38>Jun  1 08:05:04 tristram testprogram[9999]: message\n"

def test_bsd_message_builder_all_parts_counter_3():
    bsd_messages = BSDMessageBuilder("test message").priority("11").bsd_timestamp("Jan  1 00:00:01").hostname("myhost").program("myprogram").pid("1111").message("test message 2").build(counter=3)
    for bsd_message in bsd_messages:
        assert bsd_message.get_raw_message() == "<11>Jan  1 00:00:01 myhost myprogram[1111]: test message 2\n"
    assert len(bsd_messages) == 3

def test_bsd_message_remove_priority():
    bsd_message = BSDMessageBuilder("message").build()
    bsd_message.remove_priority().build()
    assert bsd_message.get_raw_message() == "Jun  1 08:05:04 tristram testprogram[9999]: message\n"
