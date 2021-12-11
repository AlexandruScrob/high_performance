from itertools import takewhile


def fibonacci_list(num_items):
    numbers = []
    a, b = 0, 1
    while len(numbers) < num_items:
        numbers.append(a)
        a, b = b, a+b
    return numbers


def fibonacci_gen(num_items):
    a, b = 0, 1
    while num_items:
        yield a
        a, b = b, a+b
        num_items -= 1


def test_fibonacci_list():
    """
    # >>> %timeit test_fibonacci_list()
    332 ms ± 13.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    #>>> %memit test_fibonacci_list()
    peak memory: 492.82 MiB, increment: 441.75 MiB
    """
    for i in fibonacci_list(100_000):
        pass


def test_fibonacci_gen():
    """
    # >>> %timeit test_fibonacci_gen()
    126 ms ± 905 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    # >>> %memit test_fibonacci_gen()
    peak memory: 51.13 MiB, increment: 0.00 MiB
    """
    for i in fibonacci_gen(100_000):
        pass


def fibonacci():
    i, j = 0, 1
    while True:
        yield j
        i, j = j, i + j


def fibonacci_naive():
    i, j = 0, 1
    count = 0
    while j <= 5000:
        if j % 2:
            count += 1
        i, j = j, i + j
    return count


def fibonacci_transform():
    count = 0
    for f in fibonacci():
        if f > 5000:
            break
        if f % 2:
            count += 1
    return count


def fibonacci_succinct():
    first_5000 = takewhile(lambda x: x <= 5000, fibonacci())
    return sum(1 for x in first_5000 if x % 2)
