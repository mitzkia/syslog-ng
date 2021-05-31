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
import asyncio
import concurrent
import socket
import threading
from abc import ABC
from abc import abstractmethod

from src.common.blocking import DEFAULT_TIMEOUT


class BackgroundEventLoop(object):
    """Singleton event loop running in the background"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BackgroundEventLoop, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop_func, daemon=True)
        self.thread.start()

    def _run_event_loop_func(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_async(self, async_func):
        return asyncio.run_coroutine_threadsafe(async_func, self.loop)

    def wait_async_result(self, async_func, timeout):
        future = self.run_async(async_func)
        try:
            return future.result(timeout=timeout)
        except (asyncio.TimeoutError, TimeoutError, concurrent.futures.TimeoutError) as err:
            future.cancel()
            raise asyncio.TimeoutError("Network operation timed out") from err

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)


class SingleConnectionStreamServer(ABC):
    def __init__(self):
        self._event_loop = BackgroundEventLoop()
        self._server = None
        self._client = self._event_loop.run_async(self._create_client()).result()

    def start(self):
        server_res = self._event_loop.run_async(self._start_server())
        self._server = server_res.result()

    def stop(self):
        self._event_loop.run_async(self._stop_server()).result()
        self.close_client()

    def close_client(self):
        """After a client connection is accepted, new connections will be rejected until this method is called"""
        self._event_loop.run_async(self._client.close()).result()

    def readexactly(self, n, timeout=DEFAULT_TIMEOUT):
        return self._event_loop.wait_async_result(self._readexactly(n), timeout=timeout)

    def readuntil(self, separator=b'\n', timeout=DEFAULT_TIMEOUT):
        return self._event_loop.wait_async_result(self._readuntil(separator), timeout=timeout)

    def readline(self, timeout=DEFAULT_TIMEOUT):
        return self._event_loop.wait_async_result(self._readline(), timeout=timeout)

    def write(self, data, timeout=DEFAULT_TIMEOUT):
        self._event_loop.wait_async_result(self._write(data), timeout=timeout)

    def get_event_loop(self):
        return self._event_loop

    async def _create_client(self):
        return self.Client()

    @abstractmethod
    async def _start_server(self):
        pass

    async def _stop_server(self):
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()

    async def _client_accepted_cb(self, reader, writer):
        self._client.accept_connection(reader, writer)

    async def _readexactly(self, n):
        await self._client.wait_for_client_connection()
        return await self._client._reader.readexactly(n)

    async def _readuntil(self, separator):
        await self._client.wait_for_client_connection()
        return await self._client._reader.readuntil(separator)

    async def _readline(self):
        await self._client.wait_for_client_connection()
        return await self._client._reader.readline()

    async def _write(self, data):
        await self._client.wait_for_client_connection()
        self._client._writer.write(data)
        await self._client._writer.drain()

    class Client(object):
        def __init__(self):
            self._connection_accepted = asyncio.Event()
            self._reader = None
            self._writer = None

        def accept_connection(self, reader, writer):
            if self._connection_accepted.is_set():
                writer.close()
                return
            self._reader = reader
            self._writer = writer
            self._connection_accepted.set()

        async def wait_for_client_connection(self):
            await self._connection_accepted.wait()

        async def close(self):
            if not self._connection_accepted.is_set():
                return
            self._writer.close()
            await self._writer.wait_closed()
            self._connection_accepted.clear()


class SingleConnectionTCPServer(SingleConnectionStreamServer):
    def __init__(self, port, host=None, ip_protocol_version=socket.AF_INET, ssl=None):
        super(SingleConnectionTCPServer, self).__init__()
        self._host = host
        self._port = port
        self._family = ip_protocol_version
        self._ssl = ssl

    async def _start_server(self):
        server = await asyncio.start_server(self._client_accepted_cb, self._host, self._port, family=self._family, ssl=self._ssl)
        await server.start_serving()
        return server


class SingleConnectionUnixStreamServer(SingleConnectionStreamServer):
    def __init__(self, path, ssl=None):
        super(SingleConnectionUnixStreamServer, self).__init__()
        self._path = path
        self._ssl = ssl

    async def _start_server(self):
        server = await asyncio.start_unix_server(self._client_accepted_cb, self._path, ssl=self._ssl)
        await server.start_serving()
        return server


class DatagramServer(ABC):
    def __init__(self):
        self._event_loop = BackgroundEventLoop()
        self._sock = None

    @abstractmethod
    def start(self):
        pass

    def stop(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def read_dgram(self, maxsize=65536, timeout=DEFAULT_TIMEOUT):
        return self._event_loop.wait_async_result(self._read_dgram(maxsize), timeout=timeout)

    def write_dgram(self, data, timeout=DEFAULT_TIMEOUT):
        return self._event_loop.wait_async_result(self._write_dgram(data), timeout=timeout)

    def get_event_loop(self):
        return self._event_loop

    async def _read_dgram(self, maxsize):
        return await self._event_loop.loop.sock_recv(self._sock, maxsize)

    async def _write_dgram(self, data):
        raise NotImplementedError


class UDPServer(DatagramServer):
    def __init__(self, port, host=None, ip_protocol_version=socket.AF_INET):
        super(UDPServer, self).__init__()
        self._host = '' if host is None else host
        self._port = port
        self._family = ip_protocol_version

    def start(self):
        self._sock = socket.socket(self._family, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setblocking(False)
        self._sock.bind((self._host, self._port))


class UnixDatagramServer(DatagramServer):
    def __init__(self, path):
        super(UnixDatagramServer, self).__init__()
        self._path = path

    def start(self):
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self._sock.setblocking(False)
        self._sock.bind(self._path)
