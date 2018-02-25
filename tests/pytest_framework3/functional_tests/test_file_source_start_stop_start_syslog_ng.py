def test_file_source_start_stop_start_syslog_ng(tc):
    # syslog-ng-1 config
    cfg = tc.new_config()
    cfg.add_global_options({"stats_level": 3, "time_reap": 1, "time_reopen": 1})
    cfg_fs = cfg.get_filesource("input")
    cfg_fd = cfg.get_filedestination("output")
    cfg.create_logpath(sources=cfg_fs, destinations=cfg_fd)

    # generate message + send
    message_counter = 1
    test_message = tc.new_bsd_message(message_parts={"program": "MYPROGRAM"}, message_counter=message_counter)
    cfg_fs.write(test_message)

    # init+start syslog-ng
    slng = tc.new_syslog_ng()
    slng.start(cfg)

    # output
    output_message = cfg_fd.read(expected_message_counter=message_counter)

    # expected_output
    expected_output_message = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM"}, expected_message_counter=message_counter)

    assert output_message == expected_output_message

    slng.stop()

    slng.start(cfg)

    test_message2 = tc.new_bsd_message(message_parts={"program": "MYPROGRAM2"}, message_counter=message_counter)
    cfg_fs.write(test_message2)

    output_message2 = cfg_fd.read_messages(expected_message_counter=2)

    # expected_output
    expected_output_message2 = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM2"}, expected_message_counter=message_counter)

    assert output_message2 == [expected_output_message, expected_output_message2]
