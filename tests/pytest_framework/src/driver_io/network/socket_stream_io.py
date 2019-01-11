#!/usr/bin/env python
#############################################################################
# Copyright (c) 2015-2019 Balabit
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

import socket
from src.driver_io.network.network import Network

class SocketStreamIO(Network):
    def __init__(self, socket_address):
        self.socket_address = socket_address #('127.0.0.1', 4444)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.received_messages = ""

    def listen(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.socket_address)
        self.socket.listen(5)
        self.socket.settimeout(1)

    def read(self):
        while True:
            try:
                client_connection, client_address = self.socket.accept()
                client_connection.settimeout(1)
                while True:
                    incoming_data = client_connection.recv(8192).decode('utf-8')
                    if incoming_data:
                        self.received_messages += incoming_data
            except socket.error:
                break
            except socket.timeout:
                break
        client_connection.close()
        self.socket.close()
        return self.received_messages

    def write(self, content):
        pass