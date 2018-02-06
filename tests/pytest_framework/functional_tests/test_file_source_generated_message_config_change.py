def test_file_source_generated_message_config_change(tc):
    # syslog-ng config
    cfg = tc.new_config()
    cfg.add_global_options({"stats_level": 3, "time_reap": 1, "time_reopen": 1})
    cfg_fs = cfg.get_filesource("input", {"follow-freq": "1"})
    cfg_fd = cfg.get_filedestination("output")
    cfg.create_logpath(sources=cfg_fs, destinations=cfg_fd)

    # generate message + send
    message_counter = 1
    test_message = tc.new_bsd_message(message_parts={"program": "MYPROGRAM1"}, message_counter=message_counter)
    cfg_fs.write(test_message)

    # start syslog-ng with config-1
    slng = tc.new_syslog_ng()
    slng.start(cfg)
    slng.dump_config()

    # change config-1 to config-2
    cfg_fs.update_file_source_options({"file_path": "input2", "follow-freq": "2"})

    # reload syslog-ng
    slng.reload(cfg)
    slng.dump_config()

    test_message2 = tc.new_bsd_message(message_parts={"program": "MYPROGRAM2"}, message_counter=message_counter)
    cfg_fs.write(test_message2)

    # output
    output_messages = cfg_fd.read_messages(expected_message_counter=2)

    # expected_output
    expected_output_message1 = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM1"}, expected_message_counter=message_counter)
    expected_output_message2 = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM2"}, expected_message_counter=message_counter)

    assert output_messages == [expected_output_message1, expected_output_message2]
