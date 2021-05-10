from statistics import median
from hypothesis import given, strategies as st
from search_median import brute_force_median

@given(long=st.lists(elements=st.floats(), min_size=1), short=st.lists(st.floats(), max_size=2))
def test_brute_foce_median(long, short):
    assert median(long + short) == brute_force_median(long, short)