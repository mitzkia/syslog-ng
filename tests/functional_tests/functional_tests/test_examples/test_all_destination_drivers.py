from source.testdb.initializer.setup_testcase import SetupTestcase

def test_use_all_destination_drivers_default(request):
    syslog_ng_tc = SetupTestcase(testcase_context=request)
    syslog_ng_tc.build_config_with_destination_drivers()
    syslog_ng_tc.run()
