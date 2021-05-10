import numpy as np
from math import floor, ceil
from statistics import median


def brute_force_median(max_4, max_2):
    med = floor((len(max_4) + len(max_2))/2)
    need_one = bool((len(max_4) + len(max_2)) % 2)
    idx_4 = 0
    idx_2 = 0
    for _ in range(med + need_one):
        if idx_2 >= len(max_2):
            first_med = max_4[idx_4]
            idx_4 += 1
        elif idx_4 >= len(max_4):
            first_med = max_2[idx_2]
            idx_2 += 1
        elif max_4[idx_4] < max_2[idx_2]:
            first_med = max_4[idx_4]
            idx_4 += 1
        else:
            first_med = max_2[idx_2]
            idx_2 += 1

    if need_one:
        return first_med

    if idx_2 >= len(max_2):
        return (first_med + max_4[idx_4])/2
    elif idx_4 >= len(max_4):
        return (first_med + max_2[idx_2])/2
    elif max_4[idx_4] < max_2[idx_2]:
        return (first_med + max_4[idx_4])/2
    return (first_med + max_2[idx_2])/2


def median_unbalanced(long_list, short_list):
    """len(short_list) <= 2!!, neither of the lists should be empty, no nan, inf
    both of them should be sorted"""
    if len(long_list) <= 4:
        return brute_force_median(long_list, short_list)
    need = 3 if len(long_list) % 2 else 4
    left_from_med = floor((len(long_list) - 1) / 2) - 1
    return brute_force_median(
        long_list[left_from_med : left_from_med + need], short_list
    )


def median_two_sorted(list_a, list_b):
    if len(list_a) < len(list_b):
        return median_reduction(list_b, list_a)
    else:
        return median_reduction(list_a, list_b)


def median_reduction(long_list, short_list):
    while len(short_list) > 2:
        short_med = (len(short_list) - 1) / 2
        short_lmed = floor(short_med)
        reduction = len(short_list) - short_lmed - 1
        long_med = (len(long_list) - 1) / 2
        if long_list[ceil(long_med)] < short_list[short_lmed]:
            long_list = long_list[reduction:]
            short_list = short_list[:-reduction]
        elif short_list[ceil(short_med)] < long_list[floor(long_med)]:
            long_list = long_list[:-reduction]
            short_list = short_list[reduction:]
        else:
            return brute_force_median(
                long_list[floor(long_med) : ceil(long_med) + 1],
                short_list[short_lmed : ceil(short_med) + 1],
            )
    return median_unbalanced(long_list, short_list)
