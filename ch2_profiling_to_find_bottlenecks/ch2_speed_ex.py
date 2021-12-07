

def fn_expressive(upper=1_000_000):
    total = 0
    for n in range(upper):
        total += n
    return total


def fn_terse(upper=1_000_000):
    return sum(range(upper))


assert fn_expressive() == fn_terse(), \
    "Expect identical results from both functions"


# PS C:\Users\User\PycharmProjects\high_performance> python -m
# timeit "import ch2_speed_ex" "ch2_speed_ex.fn_expressive()"
# 10 loops, best of 5: 31.1 msec per loop

# PS C:\Users\User\PycharmProjects\high_performance> python -m
# timeit "import ch2_speed_ex" "ch2_speed_ex.fn_terse()"
# 10 loops, best of 5: 21.4 msec per loop
