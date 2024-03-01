import time
from functools import wraps

from hyperon_das.logger import logger


def remove_none_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = [arg for arg in args if arg is not None]
        new_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        return func(*new_args, **new_kwargs)

    return wrapper


def execution_time_tracker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result, status_code = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger().info(f"The function '{func.__name__}' took {elapsed_time} seconds to execute")
        return result, status_code, elapsed_time

    return wrapper
