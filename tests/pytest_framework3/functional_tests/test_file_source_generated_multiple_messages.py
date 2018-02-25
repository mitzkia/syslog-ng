def test_file_source_generated_multiple_messages(tc):
    # syslog-ng-1 config
    cfg = tc.new_config()
    cfg_fs = cfg.get_filesource("input")
    cfg_fd = cfg.get_filedestination("output")
    cfg.create_logpath(sources=cfg_fs, destinations=cfg_fd)

    # generate messages + send
    message_counter = 6
    test_messages = tc.new_bsd_message(message_parts={"program": "MYPROGRAM"}, message_counter=message_counter)
    cfg_fs.write(test_messages)

    # init+start syslog-ng
    slng = tc.new_syslog_ng()
    slng.start(cfg)

    # output
    output_message = cfg_fd.read(expected_message_counter=message_counter)

    # expected_output
    expected_output_message = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM"}, expected_message_counter=message_counter)

    assert output_message == expected_output_message
