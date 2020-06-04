import functools
import time


class RetryError(Exception):
    pass


class TimeoutError(RetryError):
    pass


class MaxAttemptsError(RetryError):
    pass


def retry(interval, timeout=None, max_attempts=None):
    """
    The @retry decorator implements a polling mechanism on top of a generator. The decorated function should yield when
    the action is not successful and return when it is. When the function yields, the mechanism will wait `interval`
    seconds before waking up the decorated function.

    The value returned by the decorated function is returned to the caller, allowing the decorated function to produce
    a value to the caller once it has succeeded.

    If provided, the `timeout` paramater will make the function raise a TimeoutError after the given amount of seconds.
    Note that the timeout will not interrupt the generator, so if something which takes a long time is done inside of
    the generator, the timeout will not be raised until the generator yields.

    If provided, the `max_attempts` parameter will make the function raise a MaxAttemptsError after the given amount
    of attempts.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            generator = func(*args, **kwargs)
            deadline = time.monotonic() + timeout
            attempts = 0

            try:
                while True:
                    if deadline is not None and deadline < time.monotonic():
                        raise TimeoutError()

                    if max_attempts is not None and attempts >= max_attempts:
                        raise MaxAttemptsError()

                    attempts += 1
                    next(generator)
                    time.sleep(interval)
            except StopIteration as e:
                return e.value
        return wrapper

    if callable(interval):
        raise ValueError("retry decorator used without specifying interval")

    return decorator

