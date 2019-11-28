
def test_all_sources(config, syslog_ng):
    config.create_multidriver_config(parent_drivers=['default_network_drivers', 'example_diskq_source', 'example_msg_generator', 'example_random_generator', 'fifo', 'file', 'linux_audit', 'mbox', 'network', 'nodejs', 'openbsd', 'osquery', 'pacct', 'pipe', 'program', 'python', 'python_fetcher', 'snmptrap', 'stdin', 'sun_stream', 'sun_streams', 'syslog', 'systemd_journal', 'systemd_syslog', 'tcp', 'tcp6', 'udp', 'udp6', 'unix_dgram', 'unix_stream', 'wildcard_file'], driver_type="source")
    # config.create_multidriver_config(parent_drivers=['file', 'pipe', 'program', 'wildcard_file', 'tcp', 'network', 'syslog', 'tcp6', 'udp6', 'unix_stream', 'unix_dgram'], driver_type="source")
    syslog_ng.start(config)
