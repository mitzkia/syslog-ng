from src.common.findcontent import find_regexp_in_content

def test_file_source_custom_single_message(tc):
    # syslog-ng config
    cfg = tc.new_config()
    cfg_fs = cfg.get_filesource("input")
    cfg_fd = cfg.get_filedestination("output")
    cfg.create_logpath(sources=cfg_fs, destinations=cfg_fd)

    # generate custom message (without message header) + send
    test_message = "my message"
    message_counter = 1
    cfg_fs.write(test_message)

    # init+start syslog-ng
    slng = tc.new_syslog_ng()
    slng.start(cfg)

    # wait for message output
    output_message = cfg_fd.read(expected_message_counter=message_counter)

    # generate expected message output (bsd timestamp should be a regexp, because we dont know the time)
    expected_output_message = cfg_fd.get_expected_output_message(message_parts={"message": test_message, "bsd_timestamp": "regexp", "program": "skip", "pid": "skip"}, use_message_counter=False)

    # check expected and actual message
    assert expected_output_message.match(output_message)
    assert find_regexp_in_content(".*%s$" % test_message.rstrip(), output_message) is True
