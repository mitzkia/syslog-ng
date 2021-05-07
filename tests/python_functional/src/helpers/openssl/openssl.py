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
from pathlib2 import Path
from psutil import TimeoutExpired

import src.testcase_parameters.testcase_parameters as tc_parameters
from src.executors.process_executor import ProcessExecutor


class OpenSSLServer(object):

    instanceIndex = -1
    @staticmethod
    def __get_new_instance_index():
        OpenSSLServer.instanceIndex += 1
        return OpenSSLServer.instanceIndex

    def __init__(self):
        self.openssl_server_proc = None
        self.__openssl_server_stdout_path = None

    @property
    def output_path(self):
        return str(self.__openssl_server_stdout_path.absolute())

    def __decode_start_parameters(self, accept, port, key, cert):
        # TODO: other options
        start_parameters = []

        if accept is not None:
            start_parameters.extend(["-accept", accept])

        if port is not None:
            start_parameters.extend(["-port", port])

        if key is not None:
            start_parameters.extend(["-key", key])

        if cert is not None:
            start_parameters.extend(["-cert", cert])

        return start_parameters

    def start(self, accept=None, port=None, key=None, cert=None):
        if self.openssl_server_proc is not None and self.openssl_server_proc.is_running():
            raise Exception("OpenSSLServer is already running, you shouldn't call start")

        instanceIndex = OpenSSLServer.__get_new_instance_index()
        self.__openssl_server_stdout_path = Path(tc_parameters.WORKING_DIR, "openssl_server_stdout_{}".format(instanceIndex))
        openssl_server_stderr_path = Path(tc_parameters.WORKING_DIR, "openssl_server_stderr_{}".format(instanceIndex))

        self.parameters = self.__decode_start_parameters(accept, port, key, cert)

        self.openssl_server_proc = ProcessExecutor().start(
            ["openssl", "s_server"] + self.parameters,
            self.__openssl_server_stdout_path,
            openssl_server_stderr_path,
        )

        return self.openssl_server_proc

    def stop(self):
        if self.openssl_server_proc is None:
            return

        self.openssl_server_proc.terminate()
        try:
            self.openssl_server_proc.wait(4)
        except TimeoutExpired:
            self.openssl_server_proc.kill()

        self.openssl_server_proc = None
