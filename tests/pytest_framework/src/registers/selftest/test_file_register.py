import pytest
from src.registers.file import FileRegister
from src.common.random import Random

random = Random()
UNIQUE_ID = random.get_unique_id()
UNIQUE_ID2 = random.get_unique_id()


@pytest.mark.parametrize("prefix, extension, subdir, expected_result", [
    ("test_prefix", "txt", "tempdir", "/tmp/tempdir/test_prefix_{}.txt".format(UNIQUE_ID)),  # everything is defined
    ("test_prefix", "txt", None, "/tmp/test_prefix_{}.txt".format(UNIQUE_ID)),  # without subdir
])
def test_get_registered_file_path(tc_unittest, prefix, extension, subdir, expected_result):
    file_register = FileRegister(tc_unittest.logger_factory, working_dir="/tmp")
    assert file_register.get_registered_file_path(prefix, extension, subdir) == expected_result


@pytest.mark.parametrize("prefix, expected_result", [
    ("test_prefix", "/tmp/test_prefix_{}.log".format(UNIQUE_ID)),  # default extension
])
def test_get_registered_file_path_default_extension(tc_unittest, prefix, expected_result):
    file_register = FileRegister(tc_unittest.logger_factory, working_dir="/tmp")
    assert file_register.get_registered_file_path(prefix) == expected_result


def test_get_registered_file_path_key_already_registered(tc_unittest):
    file_register = FileRegister(tc_unittest.logger_factory, working_dir="/tmp")
    assert file_register.get_registered_file_path(prefix="test_prefix",
                                                  extension="txt") == "/tmp/test_prefix_{}.txt".format(UNIQUE_ID)
    assert file_register.get_registered_file_path(prefix="test_prefix",
                                                  extension="txt") == "/tmp/test_prefix_{}.txt".format(UNIQUE_ID)
    assert file_register.registered_files == {'test_prefix_txt': '/tmp/test_prefix_{}.txt'.format(UNIQUE_ID)}


def test_get_registered_file_path_same_key_different_extenstion(tc_unittest):
    file_register = FileRegister(tc_unittest.logger_factory, working_dir="/tmp")
    assert file_register.get_registered_file_path(prefix="test_prefix",
                                                  extension="txt") == "/tmp/test_prefix_{}.txt".format(UNIQUE_ID)
    assert file_register.get_registered_file_path(prefix="test_prefix",
                                                  extension="log") == "/tmp/test_prefix_{}.log".format(UNIQUE_ID2)
    assert file_register.registered_files == {
        'test_prefix_txt': '/tmp/test_prefix_{}.txt'.format(UNIQUE_ID),
        'test_prefix_log': '/tmp/test_prefix_{}.log'.format(UNIQUE_ID2),
    }
