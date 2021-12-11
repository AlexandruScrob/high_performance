from random import normalvariate, randint
from itertools import count, groupby, islice, filterfalse
from datetime import datetime
from scipy.stats import normaltest


filename = "test_1.txt"


def read_data(filename):
    with open(filename) as fd:
        for line in fd:
            data = line.strip().split(',')
            timestamp, value = map(int, data)
            yield datetime.fromtimestamp(timestamp), value


def read_fake_data(filename):
    for timestamp in count():
        # We insert an anomalous data point approximately once a week
        if randint(0, 7 * 60 * 60 * 24 - 1) == 1:
            value = normalvariate(0, 1)
        else:
            value = 100
        yield datetime.fromtimestamp(timestamp), value


def groupby_day(iterable):
    key = lambda row: row[0].day
    for day, data_group in groupby(iterable, key):
        yield list(data_group)


def is_normal(data, threshold=1e-3):
    _, values = zip(*data)
    k2, p_value = normaltest(values)
    if p_value < threshold:
        return False
    return True


def filter_anomalous_groups(data):
    yield from filterfalse(is_normal, data)


def filter_anomalous_data(data):
    data_group = groupby_day(data)
    yield from filter_anomalous_groups(data_group)


data = read_data(filename)
anomaly_generator = filter_anomalous_data(data)
first_five_anomalies = islice(anomaly_generator, 5)

for data_anomaly in first_five_anomalies:
    start_date = data_anomaly[0][0]
    end_date = data_anomaly[-1][0]
    print(f"Anomaly from {start_date} - {end_date}")

# Output of above code using "read_fake_data"
# Anomaly from 1970-01-10 00:00:00 - 1970-01-10 23:59:59
# Anomaly from 1970-01-17 00:00:00 - 1970-01-17 23:59:59
# Anomaly from 1970-01-18 00:00:00 - 1970-01-18 23:59:59
# Anomaly from 1970-01-23 00:00:00 - 1970-01-23 23:59:59
# Anomaly from 1970-01-29 00:00:00 - 1970-01-29 23:59:59


def groupby_window(data, window_size=3600):
    window = tuple(islice(data, window_size))
    for item in data:
        yield window
        window = window[1:] + (item,)
