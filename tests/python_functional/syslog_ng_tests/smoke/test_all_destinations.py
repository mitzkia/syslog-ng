
def test_all_destinations(config, syslog_ng):
    config.create_multidriver_config(parent_drivers=['amqp', 'collectd', 'elasticsearch2', 'elasticsearch_http', 'fifo', 'file', 'graphite', 'graylog2', 'hdfs', 'http', 'kafka_c', 'kafka_java', 'loggly', 'logmatic', 'mongodb', 'network', 'network_load_balancer', 'pipe', 'program', 'pseudofile', 'redis', 'riemann', 'slack', 'smtp', 'snmp', 'sql', 'stomp', 'syslog', 'tcp', 'tcp6', 'telegram', 'udp', 'udp6', 'unix_dgram', 'unix_stream'], driver_type="destination")
    # config.create_multidriver_config(parent_drivers=['file', 'pipe', 'program', 'pseudofile', 'tcp', 'tcp6', 'udp', 'udp6', 'network', 'syslog', 'unix_dgram', 'unix_stream'], driver_type="destination")
    syslog_ng.start(config)
