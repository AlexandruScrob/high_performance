# Given the following data, write an algorithm to find the
# index of the value 61:
# [9, 18, 18, 19, 29, 42, 56, 61, 88, 95]
# Since you know the data is ordered, how can you do this faster?
import bisect
import random

from ch2_profiling_to_find_bottlenecks.utils import timefn

LST = [9, 18, 18, 19, 29, 42, 56, 61, 88, 95]


@timefn
def binary_search(needle, haystack):
    imin, imax = 0, len(haystack)
    while True:
        if imin > imax:
            return -1
        midpoint = (imin + imax) // 2

        if haystack[midpoint] > needle:
            imax = midpoint
        elif haystack[midpoint] < needle:
            imin = midpoint+1
        else:
            return midpoint


def find_closest(needle, haystack):
    # bisect.bisect_left will return the first value in the haystack
    # that is greater than the needle
    i = bisect.bisect_left(haystack, needle)

    if i == len(haystack):
        return i - 1

    elif haystack[i] == needle:
        return i

    elif i > 0:
        j = i - 1
        # since we know the value is larger than needle (and vice versa
        # for the value at j), we don't need to use absolute values here
        if haystack[i] - needle > needle - haystack[j]:
            return j

    return i


important_numbers = []
for i in range(10):
    new_number = random.randint(0, 1000)
    bisect.insort(important_numbers, new_number)

print(important_numbers)


if __name__ == "__main__":
    # binary_search(61, LST)
    closest_index = find_closest(-250, important_numbers)
    print(f"Closest value to -250: {important_numbers[closest_index]}")

    closest_index = find_closest(500, important_numbers)
    print(f"Closest value to -250: {important_numbers[closest_index]}")

    closest_index = find_closest(1100, important_numbers)
    print(f"Closest value to -250: {important_numbers[closest_index]}")
