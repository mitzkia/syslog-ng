import pytest
from src.common.find_in_content import find_regexp_in_content


@pytest.mark.parametrize("regexp, content, expected_counter, expected_result", [
    (
        "^test message$",  # positive
        "test message",
        1,
        True
    ),
    (
        "^test message$",  # negative
        "test messageAAA",
        1,
        False
    ),
    (
        "^test message$",  # find double occurrence
        "test message\ntest message\n",
        2,
        True
    ),
    (
        "test message",  # non regexp will not match
        "bbb test message aaa",
        1,
        False
    ),
])
def test_find_regexp_in_content(regexp, content, expected_counter, expected_result):
    assert find_regexp_in_content(regexp, content, expected_counter) == expected_result
