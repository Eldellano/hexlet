# BEGIN
from functools import wraps


def suppress(exception, *, or_return=None):
    def wrapper(function):
        @wraps(function)
        def func(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                return or_return
        return func
    return wrapper
# END
