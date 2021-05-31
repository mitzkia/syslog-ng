#!/usr/bin/env python
#############################################################################
# Copyright (c) 2020 One Identity
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
import atexit
import socket
from enum import auto
from enum import Enum
from enum import IntEnum

from pathlib2 import Path

import src.testcase_parameters.testcase_parameters as tc_parameters
from src.common.blocking import DEFAULT_TIMEOUT
from src.common.file import File
from src.common.network_io import SingleConnectionTCPServer
from src.common.network_io import UDPServer
from src.common.random_id import get_unique_id
from src.helpers.loggen.loggen import Loggen


class NetworkIO():
    def __init__(self, ip, port, transport, ip_proto_version=None):
        self.__ip = ip
        self.__port = port
        self.__transport = transport
        self.__ip_proto_version = NetworkIO.IPProtoVersion.V4 if ip_proto_version is None else ip_proto_version
        self.__message_reader = None

        atexit.register(self.stop_listener)

    def write(self, content, rate=None):
        loggen_input_file_path = Path(tc_parameters.WORKING_DIR, "loggen_input_{}.txt".format(get_unique_id()))

        loggen_input_file = File(loggen_input_file_path)
        loggen_input_file.open(mode="w")
        loggen_input_file.write(content)
        loggen_input_file.close()

        Loggen().start(self.__ip, self.__port, read_file=str(loggen_input_file_path), dont_parse=True, permanent=True, rate=rate, **self.__transport.to_loggen_params())

    def start_listener(self):
        self.__message_reader = self.__transport.construct_reader(self.__port, self.__ip, self.__ip_proto_version)
        self.__message_reader.get_server().start()

    def stop_listener(self):
        if self.__message_reader is not None:
            self.__message_reader.get_server().stop()
            self.__message_reader = None

    def read_number_of_messages(self, counter, timeout=DEFAULT_TIMEOUT):
        return self.__message_reader.wait_for_number_of_messages(counter, timeout)

    def read_until_messages(self, lines, timeout=DEFAULT_TIMEOUT):
        return self.__message_reader.wait_for_messages(lines, timeout)

    class IPProtoVersion(IntEnum):
        V4 = socket.AF_INET
        V6 = socket.AF_INET6

    class Transport(Enum):
        TCP = auto()
        UDP = auto()
        TLS = auto()
        PROXIED_TCP = auto()
        PROXIED_TLS = auto()

        def to_loggen_params(self):
            loggen_params_mapping = {
                NetworkIO.Transport.TCP: {"inet": True, "stream": True},
                NetworkIO.Transport.UDP: {"dgram": True},
                NetworkIO.Transport.TLS: {"use_ssl": True},
                NetworkIO.Transport.PROXIED_TCP: {"inet": True, "stream": True},
                NetworkIO.Transport.PROXIED_TLS: {"use_ssl": True},
            }
            return loggen_params_mapping[self]

        def to_netcat_params(self):
            netcat_params_mapping = {
                NetworkIO.Transport.TCP: {},
                NetworkIO.Transport.UDP: {"u": True},
            }
            return netcat_params_mapping[self]

        def construct_reader(self, port, host=None, ip_proto_version=None):
            transport_mapping = {
                NetworkIO.Transport.TCP: SingleLineStreamReader(SingleConnectionTCPServer(port, host, ip_proto_version, ssl=None)),
                NetworkIO.Transport.UDP: DatagramReader(UDPServer(port, host, ip_proto_version)),
                # NetworkIO.Transport.TLS: SingleLineMessageReader(SingleConnectionTCPServer(port, host, ip_proto_version, ssl=TODO)),
                # Framed: FramedStreamReader(SingleConnectionTCPServer())
                # Frarmed TLS: FramedStreamReader(SingleConnectionTCPServer(ssl=TODO))
            }
            return transport_mapping[self]


class SingleLineStreamReader(object):
    def __init__(self, stream_server):
        self._stream_server = stream_server

    def wait_for_messages(self, lines, timeout):
        return self._stream_server.get_event_loop().wait_async_result(self._read_until_lines_found(lines), timeout=timeout)

    def wait_for_number_of_messages(self, number_of_lines, timeout):
        return self._stream_server.get_event_loop().wait_async_result(self._read_number_of_lines(number_of_lines), timeout=timeout)

    def get_server(self):
        return self._stream_server

    async def _read_until_lines_found(self, lines):
        read_lines = []
        lines_to_find = lines.copy()

        while len(lines_to_find) > 0:
            line = await self._stream_server._readline()
            if len(line) == 0:
                raise Exception("Could not find all lines. Remaining lines to find: {} Lines found: {}".format(lines_to_find, read_lines))
            line = line.decode("utf-8")
            read_lines.append(line)
            _list_remove_partially_matching_element(lines_to_find, line)
        return read_lines

    async def _read_number_of_lines(self, number_of_lines):
        lines = []
        for i in range(number_of_lines):
            line = await self._stream_server._readline()
            if len(line) == 0:
                raise Exception("Could not read {} number of lines. Connection closed after {} lines".format(number_of_lines, len(lines)))
            lines.append(line.decode("utf-8"))
        return lines


class DatagramReader(object):
    def __init__(self, datagram_server):
        self._datagram_server = datagram_server

    def wait_for_messages(self, lines, timeout, maxsize=65536):
        return self._datagram_server.get_event_loop().wait_async_result(self._read_until_dgrams_found(lines, maxsize), timeout=timeout)

    def wait_for_number_of_messages(self, number_of_msgs, timeout, maxsize=65536):
        return self._datagram_server.get_event_loop().wait_async_result(self._read_number_of_dgrams(number_of_msgs, maxsize), timeout=timeout)

    async def _read_until_dgrams_found(self, dgrams, maxsize):
        read_dgrams = []
        dgrams_to_find = dgrams.copy()

        while len(dgrams_to_find) != 0:
            dgram = await self._datagram_server._read_dgram(maxsize)
            if len(dgram) == 0:
                raise Exception("Could not find all datagrams. Remaining dgrams to find: {} Lines found: {}".format(dgrams_to_find, read_dgrams))
            dgram = dgram.decode("utf-8")
            read_dgrams.append(dgram)
            _list_remove_partially_matching_element(dgrams_to_find, dgram)
        return read_dgrams

    async def _read_number_of_dgrams(self, number_of_dgrams, maxsize):
        msgs = []
        for i in range(number_of_dgrams):
            msg = await self._datagram_server._read_dgram(maxsize)
            if len(msg) == 0:
                raise Exception("Could not read {} number of datagrams. Connection closed after {}".format(number_of_dgrams, len(msgs)))
            msgs.append(msg.decode("utf-8"))

        return msgs

    def get_server(self):
        return self._datagram_server


class FramedStreamReader(object):
    """RFC6587 message reader for the syslog() driver"""
    # TODO msg_length = readuntil(' '); msg = readexactly(msg_length)
    pass


# FileIO and this method too operate on partial string matches
# TODO: LogMessage instances should be used instead, matching the full msg body
def _list_remove_partially_matching_element(list, elem):
    for l in list:
        if l in elem:
            list.remove(l)
            return True
    return False
