import socket

class LocalSocketListener(object):
    def __init__(self, testdb_logger, local_socket_common):
        self.log_writer = testdb_logger.set_logger("LocalSocketListener")
        self.local_socket_common = local_socket_common

    def wait_for_content(self, server_address, driver_name, raw=False, message_counter=1):
        if not self.local_socket_common.is_socket_already_used(server_address):
            if driver_name in ["tcp", "tcp6", "network", "syslog", "unix-stream"]:
                return self.listen_on_socket_stream(driver_name=driver_name, message_counter=message_counter, server_address=server_address)
            elif driver_name in ["udp", "udp6", "unix-dgram"]:
                return self.listen_on_socket_dgram(driver_name=driver_name, message_counter=message_counter, server_address=server_address)
            else:
                self.log_writer.error("Unknown driver: %s" % driver_name)
                assert False
        else:
            assert False

    def listen_on_socket_stream(self, driver_name, message_counter, server_address):
        received_buffer_size = 8192
        message_arrived = False
        merged_incoming_data = ""
        generated_socket = self.local_socket_common.generate_socket_for_type(driver_name)

        generated_socket.bind(server_address)
        generated_socket.listen()
        generated_socket.settimeout(5)
        generated_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if driver_name != "unix-stream":
            generated_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
            generated_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
            generated_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        while True:
            try:
                if message_arrived:
                    break
                client_connection, client_address = generated_socket.accept()
                client_connection.settimeout(5)
                while True:
                    incoming_data = client_connection.recv(received_buffer_size).decode('utf-8')
                    merged_incoming_data += incoming_data
                    if int(merged_incoming_data.count("\n")) == int(message_counter):
                        self.log_writer.info("Expected number of messages are received on: [%s]" % str(server_address))
                        message_arrived = True
                        break
            except socket.timeout:
                generated_socket.close()
                self.log_writer.error("socket strean timeout expired: [%s], number of arrived messages: [%s]" % (str(server_address), merged_incoming_data.count("\n")))
                return merged_incoming_data

        return merged_incoming_data

    def listen_on_socket_dgram(self, driver_name, message_counter, server_address):
        received_buffer_size = 8192
        message_arrived = False
        merged_incoming_data = ""
        generated_socket = self.local_socket_common.generate_socket_for_type(driver_name)

        generated_socket.bind(server_address)
        generated_socket.settimeout(5)

        while True:
            try:
                if message_arrived:
                    break
                while True:
                    incoming_data = generated_socket.recv(received_buffer_size).decode('utf-8')
                    merged_incoming_data += incoming_data
                    if int(merged_incoming_data.count("\n")) == int(message_counter):
                        self.log_writer.info("Expected number of messages are received on: [%s]" % str(server_address))
                        message_arrived = True
                        break
            except socket.timeout:
                generated_socket.close()
                self.log_writer.error("socket dgram timeout expired: [%s], number of arrived messages: [%s]" % (str(server_address), merged_incoming_data.count("\n")))
                return merged_incoming_data

        return merged_incoming_data
