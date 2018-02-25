import pytest
from src.message.ietf_message import IETFMessage


def test_default_ietf_message_parts():
    ietf_message = IETFMessage()
    assert set(list(ietf_message.default_message_parts)) == {'priority', 'syslog_protocol_version', 'iso_timestamp',
                                                             'hostname', 'program', 'pid', 'message_id', 'sdata',
                                                             'message'}


@pytest.mark.parametrize("message_parts, expected_result", [
    (
        {
            'priority': '165', 'syslog_protocol_version': '1', 'iso_timestamp': '2003-10-11T22:14:15.003Z',
            'hostname': 'mymachine.example.com', 'program': 'evntslog', 'pid': '-', 'message_id': 'ID47',
            'sdata': '[exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"]',
            'message': 'test message'
        },
        '191 <165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"] \ufefftest message\n'
    ),
])
def test_construct_message(message_parts, expected_result):
    ietf_message = IETFMessage()
    assert ietf_message.construct_message(message_parts) == expected_result
