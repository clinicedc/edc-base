from math import ceil


def round_up(value, digits):
    ceil(value * (10 ** digits)) / (10 ** digits)
