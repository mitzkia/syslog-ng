from src.common.bufferio import BufferIO


def get_content():
    return """message 1
message 2
message3"""


def get_empty_content():
    return ""


def test_buffering_messages_fill_up_buffer():
    bufferio = BufferIO()
    bufferio.buffering_messages(get_content)
    assert bufferio.buffer == "message 1\nmessage 2\nmessage3"


def test_buffering_messages_buffer_already_contains_data():
    bufferio = BufferIO()
    bufferio.buffer = "OOO\n"
    bufferio.buffering_messages(get_content)
    assert bufferio.buffer == "OOO\nmessage 1\nmessage 2\nmessage3"


def test_buffering_messages_got_empty_data():
    bufferio = BufferIO()
    bufferio.buffering_messages(get_empty_content)
    assert bufferio.buffer == ""

def test_buffering_messages_multiple_times():
    bufferio = BufferIO()
    bufferio.buffering_messages(get_content)
    bufferio.buffering_messages(get_content)
    assert bufferio.buffer == "message 1\nmessage 2\nmessage3message 1\nmessage 2\nmessage3"

def test_parsing_messages_got_messages_with_and_without_newline():
    bufferio = BufferIO()
    bufferio.buffer = "message 1\nmessage 2\nmessage3"
    bufferio.parsing_messages()
    assert bufferio.msg_list == ["message 1\n", "message 2\n"]
    assert bufferio.buffer == "message3"


def test_parsing_messages_got_same_message_multiple_times():
    bufferio = BufferIO()
    bufferio.buffer = "message 1\nmessage 1\nmessage 1"
    bufferio.parsing_messages()
    assert bufferio.msg_list == ["message 1\n", "message 1\n"]
    assert bufferio.buffer == "message 1"


def test_parsing_messages_got_every_message_with_newline():
    bufferio = BufferIO()
    bufferio.buffer = "message 1\nmessage 2\nmessage3\n"
    bufferio.parsing_messages()
    assert bufferio.msg_list == ["message 1\n", "message 2\n", "message3\n"]
    assert bufferio.buffer == ""


def test_parsing_messages_multiple_times():
    bufferio = BufferIO()
    bufferio.buffer = "message 1\nmessage 2\nmessage3\n"
    bufferio.parsing_messages()
    bufferio.buffer = "message 1\nmessage 2\nmessage3\n"
    bufferio.parsing_messages()
    assert bufferio.msg_list == ["message 1\n", "message 2\n", "message3\n", "message 1\n", "message 2\n", "message3\n"]
    assert bufferio.buffer == ""


def test_peek_messages_with_counter_1():
    bufferio = BufferIO()
    assert bufferio.peek_msgs(get_content, 1) == ["message 1\n"]
    assert bufferio.buffer == "message3"
    assert bufferio.msg_list == ['message 1\n', 'message 2\n']
