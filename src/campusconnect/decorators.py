import functools
import logging
import time

logger = logging.getLogger("campusconnect")


def timed(func):
    """Logs how long the function took to run."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("%s took %.4fs", func.__name__, elapsed)
        return result

    return wrapper


def log_call(func):
    """Logs the function's arguments and its return value."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_text = ", ".join(
            [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        logger.info("Calling %s(%s)", func.__name__, arg_text)
        result = func(*args, **kwargs)
        logger.info("%s returned %r", func.__name__, result)
        return result

    return wrapper
