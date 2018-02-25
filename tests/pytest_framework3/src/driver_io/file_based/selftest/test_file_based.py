import pytest
from src.driver_io.file_based.interface import FileInterface
from src.driver_io.file_based.file import File
from src.driver_io.file_based.wait_for_event import FileWaitForEvent


# def instantiate_file_classes(tc_unittest):
#     temp_file = tc_unittest.file_register.get_registered_file_path("unittest_test_write_content")
#     file_object = File(tc_unittest.logger_factory, temp_file)
#     file_interface = FileInterface(tc_unittest.logger_factory)
#     return temp_file, file_object, file_interface

# def test_append_and_read_content_is_exist_and_delete_file(tc_unittest):
#     temp_file, file_object, file_interface = instantiate_file_classes(tc_unittest)

#     file_interface.write_content(temp_file, "test content 1\n")
#     file_interface.write_content(temp_file, "test content 2\n")
#     assert file_object.is_file_exist() is True
#     assert file_interface.read_content(temp_file, 2) == "test content 1\ntest content 2\n"
#     file_object.delete_file()
#     assert file_object.is_file_exist() is False


# @pytest.mark.parametrize("file_content, expected_result_lines", [
#     (
#         "test content\n",
#         1
#     ),
#     (
#         "test content\ntest content\n",
#         2
#     ),
#     (
#         "test content\ntest content",
#         1
#     ),
#     (
#         "",
#         0
#     )
# ])
# def test_get_lines(tc_unittest, file_content, expected_result_lines):
#     temp_file, file_object, file_interface = instantiate_file_classes(tc_unittest)

#     file_interface.write_content(temp_file, file_content, normalize_line_endings=False)
#     assert file_object.get_lines() == expected_result_lines
#     file_object.delete_file()


# @pytest.mark.parametrize("file_content, expected_content, expected_result", [
#     (
#         "aaa bbb ccc\n",
#         "aaa bbb cc",
#         True
#     ),
#     (
#         "aaa bbb ccc\n",
#         "aaa bbb cccc",
#         False
#     ),
#     (
#         "aaa bbb ccc\n",
#         "aaa bbb ccc",
#         True
#     ),
# ])
# def test_is_message_in_file(tc_unittest, file_content, expected_content, expected_result):
#     temp_file, file_object, file_interface = instantiate_file_classes(tc_unittest)

#     file_interface.write_content(temp_file, file_content, normalize_line_endings=False)
#     assert file_object.is_message_in_file(expected_content) is expected_result
#     file_object.delete_file()


# @pytest.mark.parametrize("file_content, expected_content, expected_result_count", [
#     (
#         "aaa bbb ccc\n",
#         "aaa",
#         1
#     ),
#     (
#         "aaa bbb ccc\n",
#         "aaa bbb",
#         1
#     ),
#     (
#         "aaa aaa aaa\n",
#         "aaa",
#         3
#     ),
#     (
#         "aaa\naaa\naaa\n",
#         "aaa",
#         3
#     ),
#     (
#         "",
#         "aaa",
#         0
#     ),
# ])
# def test_count_message_in_file(tc_unittest, file_content, expected_content, expected_result_count):
#     temp_file, file_object, file_interface = instantiate_file_classes(tc_unittest)

#     file_interface.write_content(temp_file, file_content, normalize_line_endings=False)
#     assert file_object.count_message_in_file(expected_content) is expected_result_count
#     file_object.delete_file()


@pytest.mark.parametrize("file_content, expected_content, expected_result", [
    (
        "aaa\nbbb\nccc\n",
        "bbb\n",
        True
    ),
])
def test_is_expected_message_in_buffer(tc_unittest, file_content, expected_content, expected_result):
    temp_file = tc_unittest.file_register.get_registered_file_path("unittest_test_write_content")
    file_object = File(tc_unittest.logger_factory, temp_file)
    file_interface = FileInterface(tc_unittest.logger_factory)
    file_wait_for_event = FileWaitForEvent(tc_unittest.logger_factory, temp_file)

    file_interface.write_content(temp_file, file_content, normalize_line_endings=False)
    assert file_wait_for_event.wait_for_message(expected_content) is expected_result
    file_object.delete_file()
