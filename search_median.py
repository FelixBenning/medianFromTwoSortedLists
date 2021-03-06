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
        assert self.length >= right
        self.length = right - left

    def __getitem__(self, key):
        if key < self.length:
            return self.vec[self.start + key]
        else:
            raise IndexError


def brute_force_median(list_a, list_b):
    med = floor((list_a.length + list_b.length -1) / 2)
    odd_list = bool((list_a.length + list_b.length) % 2)
    idx_a = 0
    idx_b = 0
    for _ in range(med+1):
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

    if odd_list:
        return first_med

    if idx_b >= list_b.length:
        return (first_med + list_a[idx_a]) / 2
    elif idx_a >= list_a.length:
        return (first_med + list_b[idx_b]) / 2
    elif list_a[idx_a] < list_b[idx_b]:
        return (first_med + list_a[idx_a]) / 2
    return (first_med + list_b[idx_b]) / 2


def median_two_sorted(list_a, list_b):
    a_shorter = len(list_a) < len(list_b)
    short_list = View(list_a if a_shorter else list_b)
    long_list = View(list_b if a_shorter else list_a)

    # reduce the list sizes by halving (cut_size) the short_list in every step
    while short_list.length > 1:
        short_md_idx = (short_list.length - 1) / 2
        short_left_md_idx = floor(short_md_idx)
        cut_size = short_list.length - short_left_md_idx - 1
        long_md_idx = (long_list.length - 1) / 2
        if long_list[ceil(long_md_idx)] < short_list[short_left_md_idx]:
            long_list.reduce_left(cut_size)
            short_list.reduce_right(cut_size)
        elif short_list[ceil(short_md_idx)] < long_list[floor(long_md_idx)]:
            long_list.reduce_right(cut_size)
            short_list.reduce_left(cut_size)
        else: # jackpot: overlapping medians, pick median from medians list
            long_list.reduce_slice(floor(long_md_idx), ceil(long_md_idx) + 1)
            short_list.reduce_slice(short_left_md_idx, ceil(short_md_idx) + 1)
            return brute_force_median(long_list, short_list)

    # at this point the short_list only contains one element
    if long_list.length <= 3: # long_list is also short
        return brute_force_median(long_list, short_list)
    
    # the short_list can only shift the median of the long_list by at most one
    # since it only has one element. We need 3 elements from an odd list
    # or 2 from an even list (padding around the median)
    left_median = floor((long_list.length - 1) / 2)
    long_list.reduce_slice(left_median - long_list.length % 2, left_median +2)
    return brute_force_median(long_list, short_list)
