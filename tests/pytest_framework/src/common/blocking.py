import time

MONITORING_TIME = 10
POLL_FREQ = 0.001


def wait_until_stabilized(func, args=None, monitoring_time=MONITORING_TIME):
    equal_counter = 0
    expected_equal_counter = 100
    t_end = time.monotonic() + monitoring_time
    while time.monotonic() <= t_end:
        if args:
            result_before = func(args)
            time.sleep(POLL_FREQ)
            result_after = func(args)
        else:
            result_before = func()
            time.sleep(POLL_FREQ)
            result_after = func()
        if result_before == result_after:
            equal_counter += 1
        if equal_counter == expected_equal_counter:
            return True
    return False


def wait_until_true(func, *args, monitoring_time=MONITORING_TIME):
    t_end = time.monotonic() + monitoring_time
    while time.monotonic() <= t_end:
        result = func(*args)
        if result:
            return result
        time.sleep(POLL_FREQ)
    return False

def wait_until_false(func, *args, monitoring_time=MONITORING_TIME):
    negate = lambda func, *args: not func(*args)
    return wait_until_true(negate, func, *args)
