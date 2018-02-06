import time

MONITORING_TIME = 10
poll_freq = 0.001


def wait_till_before_after_not_equals(func, args=None, monitoring_time=MONITORING_TIME):
    equal_counter = 0
    expected_equal_counter = 100
    t_end = time.monotonic() + monitoring_time
    while time.monotonic() <= t_end:
        if args:
            result_before = func(args)
            time.sleep(poll_freq)
            result_after = func(args)
        else:
            result_before = func()
            time.sleep(poll_freq)
            result_after = func()
        if result_before == result_after:
            equal_counter += 1
        if equal_counter == expected_equal_counter:
            return True
    return False


def wait_till_function_not_true(func, *args, monitoring_time=MONITORING_TIME):
    t_end = time.monotonic() + monitoring_time
    while time.monotonic() <= t_end:
        if args:
            if func(*args):
                return True
        else:
            if func():
                return True
        time.sleep(poll_freq)
    return False


def wait_till_function_not_false(func, *args, monitoring_time=MONITORING_TIME):
    t_end = time.monotonic() + monitoring_time
    while time.monotonic() <= t_end:
        if args:
            if not func(*args):
                return True
        else:
            if not func():
                return True
        time.sleep(poll_freq)
    return False
