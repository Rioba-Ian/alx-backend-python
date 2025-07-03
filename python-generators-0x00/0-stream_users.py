from itertools import islice


def stream_users():
    for user in islice(stream_users(), 10):
        yield user
