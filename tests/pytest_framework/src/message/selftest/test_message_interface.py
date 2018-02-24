from src.message.message_interface import MessageInterface

def test_a(tc_unittest):
    message_interface = MessageInterface(tc_unittest.logger_factory)
    assert "AAA" == message_interface.create_bsd_message()