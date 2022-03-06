import pytest

from lazy_interval_tree import Interval, LazyIntervalTree


def test_merge_overlaps():
    intervals = [Interval(3, 10, "hello"), Interval(1, 11, "good")]
    tree = LazyIntervalTree(intervals)
    print(tree.intervals)
    tree.merge_overlaps(data_combiner=list)
    print(tree.intervals)


@pytest.mark.parametrize(
    "test_case,intervals,expected",
    [
        (
            "two-separate-intervals",
            [Interval(3, 5, "good"), Interval(1, 2, "hello")],
            [Interval(begin=1, end=2, data={"hello"}), Interval(begin=3, end=5, data={"good"}),],
        ),
        (
            "two-touching-intervals",
            [Interval(3, 5, "good"), Interval(1, 3, "hello")],
            [Interval(begin=1, end=3, data={"hello"}), Interval(begin=3, end=5, data={"good"}),],
        ),
        (
            "two-overlapping-intervals",
            [Interval(1, 4, "hello"), Interval(3, 5, "good")],
            [
                Interval(begin=1, end=3, data={"hello"}),
                Interval(begin=3, end=4, data={"hello", "good"}),
                Interval(begin=4, end=5, data={"good"}),
            ],
        ),
        (
            "two-matching-intervals",
            [Interval(1, 4, "hello"), Interval(1, 4, "good")],
            [Interval(begin=1, end=4, data={"hello", "good"}),],
        ),
        (
            "one-interval-contains-another",
            [Interval(3, 10, "hello"), Interval(1, 11, "good")],
            [
                Interval(begin=1, end=3, data={"good"}),
                Interval(begin=3, end=10, data={"hello", "good"}),
                Interval(begin=10, end=11, data={"good"}),
            ],
        ),
        (
            "one-interval-starts-another",
            [Interval(1, 10, "hello"), Interval(1, 11, "good")],
            [Interval(begin=1, end=10, data={"hello", "good"}), Interval(begin=10, end=11, data={"good"}),],
        ),
        (
            "one-interval-finishes-another",
            [Interval(3, 11, "hello"), Interval(1, 11, "good")],
            [Interval(begin=1, end=3, data={"good"}), Interval(begin=3, end=11, data={"hello", "good"}),],
        ),
    ],
)
def test_split_overlaps(test_case, intervals, expected):
    tree = LazyIntervalTree(intervals)

    def set_union(a, b):
        return a | b

    tree.split_overlaps(data_combiner=set_union)
    assert expected == tree.intervals
