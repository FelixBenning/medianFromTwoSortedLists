from statistics import median
from hypothesis import given, strategies as st, example
from search_median import median_two_sorted, View


@given(
    list_a=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
    list_b=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
)
@example(list_a=[0.0, 0.0, 0.0], list_b=[0.0, -1.0, -1.0])
def test_median_two_sorted(list_a, list_b):
    list_a.sort()
    list_b.sort()
    assert median(list_a + list_b) == median_two_sorted(list_a, list_b)
