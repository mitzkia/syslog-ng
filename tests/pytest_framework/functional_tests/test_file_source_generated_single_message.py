def test_file_source_generated_message(tc):
    # syslog-ng-1 config
    cfg = tc.new_config()
    cfg.add_global_options({"stats_level": 3})
    cfg_fs = cfg.get_filesource("input")
    cfg_fd = cfg.get_filedestination("output")
    cfg_fd2 = cfg.get_filedestination("output2")
    cfg_fd3 = cfg.get_filedestination("output3")
    cfg.create_logpath(sources=cfg_fs, destinations=[cfg_fd, cfg_fd2, cfg_fd3])

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
    assert cfg_fd.get_query() == {'memory_usage': 0, 'written': message_counter, 'processed': message_counter, 'dropped': 0, 'queued': 0}
    assert cfg_fs.get_query()["processed"] == message_counter

    slng.syslog_ng_ctl.check_stats_and_query_counters(cfg.syslog_ng_config, destination_counter_values={
        "processed": message_counter,
        "written": message_counter,
        "dropped": 0,
        "queued": 0,
        "memory_usage": 0
    }, source_counter_values = {
        "processed": message_counter
    })
