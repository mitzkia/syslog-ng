def test_core_file_detection(tc):
    cfg = tc.new_config()
    cfg.create_logpath(sources=None, destinations=None, flags="flow_control")

    slng = tc.new_syslog_ng()
    slng.start(cfg, expected_run=False)
