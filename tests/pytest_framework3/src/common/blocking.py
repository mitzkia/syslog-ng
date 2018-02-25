import time

MONITORING_TIME = 10
POLL_FREQ = 0.001


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
    return wait_until_true(negate, func, *args, monitoring_time=monitoring_time)
