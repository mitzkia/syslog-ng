from src.common.findcontent import find_regexp_in_content
from src.driverio.fileio import FileIO


def test_file_source_with_raw_config(tc):
    fileio = FileIO(tc.logger_factory)
    src_file = tc.new_file_path(prefix="input")
    dst_file = tc.new_file_path(prefix="output")
    cfg = tc.new_config()
    raw_config = """@version: %s
options{stats_level(3);};
log {
        source { file("%s" flags(no-parse) ); };
        if (message("almafa")) {
                destination { file("%s" persist-name('aaa') template(">>>>ALMA<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
        } elif (message("belafa")) {
                if (message("magja")) {
                        destination { file("%s" persist-name('bbb1') template(">>>>BELA MAG<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
                } elif (message("termese")) {
                        destination { file("%s" persist-name('bbb2') template(">>>>BELA TERMES<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
                } elif (message("levele")) {
                        destination { file("%s" persist-name('bbb3') template(">>>>BELA LEVEL<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
                };
        } elif (message("celafa")) {
                destination { file("%s" persist-name('ccc') template(">>>>CELA<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
        } else {
                destination { file("%s" persist-name('xxx') template(">>>>XXXX<<<< $ISODATE $HOST $MSGHDR$MSG\n")); };
        };
};""" % (tc.runtime_parameters["syslog_ng_version"], src_file, dst_file, dst_file, dst_file, dst_file, dst_file, dst_file)
    cfg.set_raw_config(raw_config)

    fileio.write(file_path=src_file, content="almafa")
    fileio.write(file_path=src_file, content="belafa")
    fileio.write(file_path=src_file, content="celafa")
    fileio.write(file_path=src_file, content="test")
    fileio.write(file_path=src_file, content="belafa magja")
    fileio.write(file_path=src_file, content="belafa termese")
    fileio.write(file_path=src_file, content="belafa levele")

    slng = tc.new_syslog_ng()
    slng.start(cfg)

    dst_file_content = fileio.read_file(file_path=dst_file, expected_message_counter=6)

    assert find_regexp_in_content("^>>>>ALMA<<<<.*almafa$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>BELA MAG<<<<.*belafa magja$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>BELA TERMES<<<<.*belafa termese$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>BELA LEVEL<<<<.*belafa levele$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>CELA<<<<.*celafa$", dst_file_content) is True
    assert find_regexp_in_content("^>>>>XXXX<<<<.*test$", dst_file_content) is True
    assert find_regexp_in_content("^.*belafa$", dst_file_content) is False
