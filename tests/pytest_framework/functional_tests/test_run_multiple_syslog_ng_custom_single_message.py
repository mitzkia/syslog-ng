def test_multiple_syslog_ng(tc):
    # config for server instance
    cfg = tc.new_config(instance_name="server")
    cfg_fs = cfg.get_filesource("input")
    cfg_fs2 = cfg.get_filesource("input2")
    cfg_fd = cfg.get_filedestination("output")
    logpath = cfg.create_logpath(sources=cfg_fs, destinations=cfg_fd)
    logpath.add_source(cfg_fs2)

    # config for client instance
    cfg2 = tc.new_config(instance_name="client")
    cfg2_fs = cfg2.get_filesource("input2")
    cfg2_fd = cfg2.get_filedestination("output2")
    cfg2.create_logpath(sources=cfg2_fs, destinations=cfg2_fd)

    # generate message + send for server instance
    test_message = "my message"
    cfg_fs.write(test_message)

    # init+start syslog-ng for server instance
    slng = tc.new_syslog_ng(instance_name="server")
    slng.start(cfg)

    # init+start syslog-ng for client instance
    slng2 = tc.new_syslog_ng(instance_name="client")
    slng2.start(cfg2)

    output_message = cfg_fd.read()
    assert test_message in output_message

    assert "AAA" == "VVVVV"
