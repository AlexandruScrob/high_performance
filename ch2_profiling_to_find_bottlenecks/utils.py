import time
from functools import wraps


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time_ns()
        result = fn(*args, **kwargs)
        t2 = time.time_ns()
        print(f"@timefn: {fn.__name__} took {t2 - t1} seconds")
        return result
    return measure_time


# check for profiler in the local scope, both
# are injected by their respective tools or they're absent
# if these tools aren't being used (in which case we need to substitute
# a dummy @profile decorator)
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            from line_profiler import LineProfiler
            prof = LineProfiler()
            try:
                return prof(func)(*args, **kwargs)
            finally:
                prof.print_stats()

        return wrapper
