from statistics import median
import numpy as np
from hypothesis import given, strategies as st, example
from search_median import median_unbalanced, median_two_sorted


@given(
    long=st.lists(
        elements=st.floats(allow_nan=False, allow_infinity=False), min_size=1
    ),
    short=st.lists(
        st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=2
    ),
)
@example(long=[0.0], short=[0.0])
def test_median_unbalanced(long, short):
    long.sort()
    short.sort()
    assert median(long + short) == median_unbalanced(np.array(long), np.array(short))


@given(
    list_a=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    list_b=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
)
@example(list_a=[0.0], list_b=[0.0, -1.0])
def test_median_two_sorted(list_a, list_b):
    list_a.sort()
    list_b.sort()
    assert median(list_a + list_b) == median_two_sorted(
        np.array(list_a), np.array(list_b)
    )
