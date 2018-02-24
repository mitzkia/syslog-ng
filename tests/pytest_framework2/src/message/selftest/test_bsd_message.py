import pytest
from src.message.bsd_message import BSDMessage


def test_default_bsd_message_parts():
    bsd_message = BSDMessage()
    assert set(list(bsd_message.default_message_parts)) == {'priority', 'bsd_timestamp', 'hostname', 'program', 'pid',
                                                            'message'}


@pytest.mark.parametrize("message_parts, expected_result", [
    (
        {"priority": "42", "bsd_timestamp": "Jun  1 08:05:42", "hostname": "testhost", "program": "testprogram",
            "pid": "9999", "message": "test message"},
        "<42>Jun  1 08:05:42 testhost testprogram[9999]: test message\n"
    ),
    (
        {"message": "test message\n"},
        "test message\n"
    ),
])
def test_construct_message(message_parts, expected_result):
    bsd_message = BSDMessage()
    assert bsd_message.construct_message(message_parts) == expected_result
