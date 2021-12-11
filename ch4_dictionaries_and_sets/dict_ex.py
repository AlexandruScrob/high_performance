import string
import timeit


# Dictionary lookup sequence
def index_sequence(key, mask=0b111, PERTURB_SHIFT=5):
    perturb = hash(key)
    i = perturb & mask
    yield i

    while True:
        perturb >>= PERTURB_SHIFT
        i = (i * 5 + perturb + 1) & mask
        yield i


# Custom hashing function
class City(str):
    def __hash__(self):
        return ord(self[0])


# We create a dictionary where we assign arbitrary values to cities
data = {
    City("Rome"): 'Italy',
    City("San Francisco"): 'USA',
    City("New York"): 'USA',
    City("Barcelona"): 'Spain',
}

print(hash("Barcelona"), hash("Rome"))


# Optimal two-letter hashing function
def twoletter_hash(key):
    offset = ord('a')
    k1, k2 = key
    return (ord(k2) - offset) + 26 * (ord(k1) - offset)


class BadHash(str):
    def __hash__(self):
        return 42


class GoodHash(str):
    def __hash__(self):
        """
        This is a slightly optimized version of twoletter_hash
        """
        return ord(self[1]) + 26 * ord(self[0]) - 2619


baddict = set()
gooddict = set()
for i in string.ascii_lowercase:
    for j in string.ascii_lowercase:
        key = i + j

        baddict.add(BadHash(key))
        gooddict.add(GoodHash(key))


badtime = timeit.repeat(
    "key in baddict",
    setup="from __main__ import baddict, BadHash; key = BadHash('zz')",
    repeat=3,
    number=1_000_000,
)

goodtime = timeit.repeat(
    "key in gooddict",
    setup="from __main__ import gooddict, GoodHash; key = GoodHash('zz')",
    repeat=3,
    number=1_000_000,
)


print(f"Min lookup time for baddict: {min(badtime)}")
print(f"Min lookup time for gooddict: {min(goodtime)}")

# Results:
# Min lookup time for baddict: 9.642472399999999
# Min lookup time for gooddict: 0.20104500000000058
