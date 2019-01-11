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

from src.message_reader.message_reader import MessageReader
from src.message_reader.single_line_parser import SingleLineParser
from multiprocessing import Process, Manager

class DestinationDriver(object):
    def __init__(self, logger_factory, IOClass):
        self.__logger_factory = logger_factory
        self.__logger = logger_factory.create_logger("DestinationDriver")
        self.__IOClass = IOClass
        self.__reader = None

    def dd_read_logs(self, path, counter):
        if not self.__reader:
            io = self.__IOClass(self.__logger_factory, path)
            io.wait_for_creation()
            message_reader = MessageReader(
                self.__logger_factory, io.read, SingleLineParser(self.__logger_factory)
            )
            self.__reader = message_reader
        messages = self.__reader.pop_messages(counter)
        self.__logger.print_io_content(path, messages, "Content has been read from")
        return messages

    def dd_start_listen(self, socket, counter):
        self.native_driver_io = self.__native_driver_io_ref(socket)
        self.native_driver_io.listen()
        message_reader = MessageReader(
                self.__logger_factory, self.native_driver_io.read, SingleLineParser(self.__logger_factory)
            )
        self.p = Process(target=message_reader.pop_messages, args=(counter,self.received_messages, ))
        self.p.start()

    def dd_stop_listen(self):
        self.p.join()

    def dd_received_socket_messages(self):
        return self.received_messages