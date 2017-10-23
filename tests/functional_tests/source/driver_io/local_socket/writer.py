class LocalSocketWriter(object):
    def __init__(self, testdb_logger, local_socket_common):
        self.testdb_logger = testdb_logger
        self.log_writer = testdb_logger.set_logger("LocalSocketWriter")
        self.local_socket_common = local_socket_common

    # High level functions
    def write_content(self, client_address, content, driver_name):
        if driver_name in ["tcp", "syslog", "network", "unix-stream", "tcp6"]:
            self.send_content_to_stream(driver_name=driver_name, client_address=client_address, content=content)
        elif driver_name in ["udp", "udp6", "unix-dgram"]:
            self.send_content_to_dgram(driver_name=driver_name, client_address=client_address, content=content)
        else:
            self.log_writer.error("Unknown driver: %s" % driver_name)
            assert False

    def send_content_to_tcp_socket(self, client_address, content):
        self.send_content_to_stream(driver_name="tcp", client_address=client_address, content=content)

    def send_content_to_udp_socket(self, client_address, content):
        self.send_content_to_dgram(driver_name="udp", client_address=client_address, content=content)

    # Low level functions
    def send_content_to_stream(self, driver_name, client_address, content):
        self.local_socket_common.wait_for_socket_listening(driver_name, client_address)

        client_socket = self.local_socket_common.generate_socket_for_type(driver_name=driver_name)
        client_socket.connect((client_address))
        try:
            if isinstance(content, list):
                for line in content:
                    result = client_socket.sendall(str.encode(line))
            else:
                result = client_socket.sendall(str.encode(content))
        except OSError:
            self.log_writer.error("Can not send content to stream socket, maybe it was not available")
            assert False

        self.testdb_logger.write_message_based_on_value(logsource=self.log_writer, message="Content [%s] has been sent to stream client, socket type: [%s], socket data: [%s]" % (content, driver_name, client_address), value=(result is None))
        client_socket.close()
        if result is not None:
            assert False

    def send_content_to_dgram(self, driver_name, client_address, content):
        self.local_socket_common.wait_for_socket_listening(driver_name, client_address)

        client_socket = self.local_socket_common.generate_socket_for_type(driver_name=driver_name)
        client_socket.connect((client_address))
        try:
            if isinstance(content, list):
                for line in content:
                    result = client_socket.sendall(str.encode(line))
            else:
                result = client_socket.sendall(str.encode(content))
        except OSError:
            self.log_writer.error("Can not send content to dgram socket, maybe it was not available")
            assert False

        self.testdb_logger.write_message_based_on_value(logsource=self.log_writer, message="Content [%s] has been sent to dgram client, socket type: [%s], socket data: [%s]" % (content, driver_name, client_address), value=(result is None))
        client_socket.close()
        if result is not None:
            assert False
