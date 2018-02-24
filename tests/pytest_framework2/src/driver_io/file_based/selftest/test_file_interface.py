from src.driver_io.file_based.fileinterface import FileInterface
from src.driver_io.file_based.file import File

def instantiate_file_classes(tc_unittest):
    temp_file = tc_unittest.file_register.get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.logger_factory, temp_file)
    file_interface = FileInterface(tc_unittest.logger_factory)
    return temp_file, file_object, file_interface

def test_write_content(tc_unittest):
    temp_file, file_object, file_interface = instantiate_file_classes(tc_unittest)

    file_interface.write_content(temp_file, "test content\n")
    assert file_object.is_file_exist() is True
    assert file_interface.read_content(temp_file, 1) == "test content\n"
    file_object.delete_file()
    assert file_object.is_file_exist() is False
