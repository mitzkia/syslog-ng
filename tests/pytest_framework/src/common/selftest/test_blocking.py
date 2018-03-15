import pytest
from src.common.blocking import wait_until_true

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)

def inner_function_return_true():
    for counter in range(0, 10):
        print("\nCounter in internal function: {}".format(counter))
    return True

def inner_function_return_false():
    for counter in range(0, 10):
        print("\nCounter: {}".format(counter))
    return False

def inner_function_with_wait_until_true():
    inner = False
    while not inner:
        print("AAAA")
    # for counter in range(0, 10):
        # print("\nCounter in external function: {}".format(counter))
        if not inner:
            wait_until_true(inner_function_return_false, monitoring_time=1)
            inner = True
    return True

# def test_wait_until_true_one_inner_function_with_return_true():
#     assert wait_until_true(inner_function_return_true)

def test_double_wait_until_true_with_both_returns_with_true():
    assert wait_until_true(inner_function_with_wait_until_true, monitoring_time=1)

# @slow
# def test_wait_until_true_one_inner_function_with_return_false():
#     assert wait_until_true(inner_function_return_false, monitoring_time=1) == False