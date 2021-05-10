from statistics import median
from hypothesis import given, strategies as st, example
from search_median import median_unbalanced


@given(
    long=st.lists(
        elements=st.floats(allow_nan=False, allow_infinity=False), min_size=1
    ),
    short=st.lists(
        st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=2
    ),
)
@example(long=[0.0, 0.0, 0.0, -1.0, 0.0], short=[-1.0])
def test_median_unbalanced(long, short):
    long.sort()
    short.sort()
    assert median(long + short) == median_unbalanced(long, short)
