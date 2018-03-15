def test_minimal(tc):
    cfg = tc.new_config()
    cfg_fs = cfg.get_filesource("input")
    cfg_fd = cfg.get_filedestination("output")
    cfg.create_logpath(sources=cfg_fs, destinations=cfg_fd)
    # cfg.create_logpath(sources=None, destinations=None)

    # message_counter = 3
    # test_messages = tc.new_bsd_message(message_parts={"program": "MYPROGRAM"}, message_counter=message_counter)
    # cfg_fs.write(test_messages)

    slng = tc.new_syslog_ng()
    # slng.start(cfg, external_tool="valgrind")
    slng.start(cfg)
    # print("****************************1")
    # slng.reload(cfg)
    # # print("****************************2")
    # slng.reload(cfg)
    # # # print("****************************3")
    # # slng.start(cfg, external_tool='valgrind')
    # #
    # message_counter = 2
    # test_messages = tc.new_bsd_message(message_parts={"program": "MYPROGRAM"}, message_counter=message_counter)
    # #
    # cfg_fs.write(test_messages)
    # #
    # slng.reload(cfg)
    # slng.stop()
    # #
    # slng.start(cfg)
    # # output
    # output_message = cfg_fd.read(expected_message_counter=message_counter)
    # #
    # # # expected_output
    # expected_output_message = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM"}, expected_message_counter=message_counter)
    # #
    # assert output_message == expected_output_message
    # #
    # #
    # cfg_fs.write(test_messages)
    
    # output_message = cfg_fd.read(expected_message_counter=message_counter)
    
    # # expected_output
    # expected_output_message = cfg_fd.get_expected_output_message(message_parts={"program": "MYPROGRAM"}, expected_message_counter=message_counter)
    
    # assert output_message == expected_output_message
