def test_pipe_source_generated_message(tc):
    # syslog-ng-1 config
    cfg = tc.new_config()
    cfg.add_global_options({"stats_level": 3})
    cfg_ps = cfg.get_pipesource("input")
    cfg_pd = cfg.get_pipedestination("output")
    cfg.create_logpath(sources=cfg_ps, destinations=cfg_pd)

    # generate message + send
    message_counter = 1
    test_message = tc.new_bsd_message(message_parts={"hostname": "skip", "program": "MYPROGRAM"}, message_counter=message_counter)

    # init+start syslog-ng
    slng = tc.new_syslog_ng()
    slng.start(cfg)

    cfg_ps.write(test_message)

    # output
    output_message = cfg_pd.read()

    # expected_output
    expected_output_message = cfg_pd.get_expected_output_message(message_parts={"program": "MYPROGRAM"}, expected_message_counter=message_counter)

    assert output_message == expected_output_message
    assert cfg_pd.get_query() == {'memory_usage': 0, 'written': message_counter, 'processed': message_counter, 'dropped': 0, 'queued': 0}
    assert cfg_ps.get_query()["processed"] == message_counter

    slng.syslog_ng_ctl.check_stats_and_query_counters(cfg.syslog_ng_config, destination_counter_values={
        "processed": message_counter,
        "written": message_counter,
        "dropped": 0,
        "queued": 0,
        "memory_usage": 0
    }, source_counter_values={
        "processed": message_counter
    })
