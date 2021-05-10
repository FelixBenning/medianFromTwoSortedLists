from math import floor, ceil
from statistics import median


class View:
    def __init__(self, vec):
        self.vec = vec
        self.start = 0
        self.length = len(vec)

    def reduce_left(self, amount):
        self.start += amount
        self.length -= amount

    def reduce_right(self, amount):
        self.length -= amount

    def reduce_slice(self, left, right):
        self.start += left
        assert self.length > right
        self.length = right - left

    def reduce_to(self, left, size):
        self.start += left
        self.length = size

    def __getitem__(self, key):
        if key < self.length:
            return self.vec[self.start + key]
        else:
            raise IndexError


def brute_force_median(list_a, list_b):
    med = floor((list_a.length + list_b.length) / 2)
    need_one = bool((list_a.length + list_b.length) % 2)
    idx_a = 0
    idx_b = 0
    for _ in range(med + need_one):
        if idx_b >= list_b.length:
            first_med = list_a[idx_a]
            idx_a += 1
        elif idx_a >= list_a.length:
            first_med = list_b[idx_b]
            idx_b += 1
        elif list_a[idx_a] < list_b[idx_b]:
            first_med = list_a[idx_a]
            idx_a += 1
        else:
            first_med = list_b[idx_b]
            idx_b += 1

    if need_one:
        return first_med

    if idx_b >= list_b.length:
        return (first_med + list_a[idx_a]) / 2
    elif idx_a >= list_a.length:
        return (first_med + list_b[idx_b]) / 2
    elif list_a[idx_a] < list_b[idx_b]:
        return (first_med + list_a[idx_a]) / 2
    return (first_med + list_b[idx_b]) / 2


def median_unbalanced(long_list, short_list):
    """len(short_list) <= 2!!, neither of the lists should be empty, no nan, inf
    both of them should be sorted"""
    if long_list.length <= 4:
        return brute_force_median(long_list, short_list)
    need = 3 if long_list.length % 2 else 4
    left_from_med = floor((long_list.length - 1) / 2) - 1
    long_list.reduce_to(left_from_med, need)
    return brute_force_median(long_list, short_list)


def median_two_sorted(list_a, list_b):
    if len(list_a) < len(list_b):
        return median_reduction(View(list_b), View(list_a))
    else:
        return median_reduction(View(list_a), View(list_b))


def median_reduction(long_list, short_list):
    while short_list.length > 2:
        short_med = (short_list.length - 1) / 2
        short_lmed = floor(short_med)
        reduction = short_list.length - short_lmed - 1
        long_med = (long_list.length - 1) / 2
        if long_list[ceil(long_med)] < short_list[short_lmed]:
            long_list.reduce_left(reduction)
            short_list.reduce_right(reduction)
        elif short_list[ceil(short_med)] < long_list[floor(long_med)]:
            long_list.reduce_right(reduction)
            short_list.reduce_left(reduction)
        else:
            long_list.reduce_slice(floor(long_med), ceil(long_med) + 1)
            short_list.reduce_slice(short_lmed, ceil(short_med) + 1)
            return brute_force_median(long_list, short_list)
    return median_unbalanced(long_list, short_list)
