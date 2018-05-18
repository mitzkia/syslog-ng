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


class DriverBase(object):

    def __init__(self, statement, driver, option_setter):
        self.statement = statement
        self.driver = driver
        self.option_setter = option_setter

    def get_statement(self):
        return self.statement

    def get_statement_id(self):
        return self.statement.node_id

    def get_statement_node(self):
        return self.statement.created_node

    def get_driver(self):
        return self.driver

    def get_option_setter(self):
        return self.option_setter
