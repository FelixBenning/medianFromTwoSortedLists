import numpy as np
from math import floor
from statistics import median


def brute_force_median(max_4, max_2):
    return median(np.concatenate((max_4, max_2)))


def median_unbalanced(long_list, short_list):
    """len(short_list) <= 2!!, neither of the lists should be empty, no nan, inf"""
    if len(long_list) <= 4:
        return brute_force_median(long_list, short_list)
    med = (len(long_list) - 1) / 2
    lmed = floor(med)
    need = 3 if lmed == med else 4
    return brute_force_median(
        long_list[lmed - 1: lmed -1 + need], short_list
    )

