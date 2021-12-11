import math
from math import sin


# Namespace lookups
def test1(x):
    """
    # >>> %timeit test1(123_456)
    162 μs ± 3.82 μs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    res = 1
    for _ in range(1000):
        res += math.sin(x)

    return res


def test2(x):
    """
    # >>> %timeit test2(123_456)
    124 μs ± 6.77 μs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    res = 1
    for _ in range(1000):
        res += sin(x)

    return res


def test3(x, sin=math.sin):
    """
    # >>> %timeit test3(123_456)
    105 μs ± 3.35 μs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    res = 1
    for _ in range(1000):
        res += sin(x)

    return res


