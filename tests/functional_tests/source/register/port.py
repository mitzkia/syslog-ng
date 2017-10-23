import random


class PortRegister(object):
    def __init__(self, testdb_logger):
        self.log_writer = testdb_logger.set_logger("PortRegister")
        self.registered_tcp_ports = {}
        self.registered_udp_ports = {}
        self.min_port = 49152
        self.max_port = 65535

    def get_registered_tcp_port(self, prefix):
        if self.is_prefix_already_registered_for_pool(prefix, self.registered_tcp_ports):
            return self.registered_tcp_ports[prefix]
        else:
            while True:
                uniq_tcp_port = self.generate_random_port()
                if not self.is_port_already_used_in_pool(uniq_tcp_port, self.registered_tcp_ports):
                    break
            self.register_port_in_pool(prefix, uniq_tcp_port, self.registered_tcp_ports)
            return uniq_tcp_port

    def get_registered_udp_port(self, prefix):
        if self.is_prefix_already_registered_for_pool(prefix, self.registered_udp_ports):
            return self.registered_udp_ports[prefix]
        else:
            while True:
                uniq_udp_port = self.generate_random_port()
                if not self.is_port_already_used_in_pool(uniq_udp_port, self.registered_udp_ports):
                    break
            self.register_port_in_pool(prefix, uniq_udp_port, self.registered_udp_ports)
            return uniq_udp_port

    def is_prefix_already_registered_for_pool(self, prefix, pool):
        return prefix in pool.keys()

    def is_port_already_used_in_pool(self, port, pool):
        return port in pool.values()

    def generate_random_port(self):
        return random.randint(self.min_port, self.max_port)

    def register_port_in_pool(self, prefix, port, pool):
        pool[prefix] = port
        self.log_writer.debug("Uniq port has been registered with prefix: prefix: [%s], port: [%s]", prefix, port)
