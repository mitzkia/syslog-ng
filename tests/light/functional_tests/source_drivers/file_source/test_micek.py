import time

def test_micek1(config, syslog_ng):
    print(">>> test-start\n")
    assert True
    file_source = config.create_file_source(file_name="input.log")
    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[file_source, file_destination])
    syslog_ng.start(config)
    file_source.write_log("aaaaaa\n", 1)
    time.sleep(1)
    print(">>> test-finish\n")


def test_micek2(config, syslog_ng):
    print(">>> test-start\n")
    assert True
    file_source = config.create_file_source(file_name="input.log")
    file_destination = config.create_file_destination(file_name="output.log")
    config.create_logpath(statements=[file_source, file_destination])
    syslog_ng.start(config)
    file_source.write_log("aaaaaa\n", 1)
    time.sleep(1)
    print(">>> test-finish\n")