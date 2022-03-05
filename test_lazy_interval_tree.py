from lazy_interval_tree import Interval, LazyIntervalTree


def test_merge_intervals():
    intervals = [Interval(3, 10, "hello"), Interval(1, 11, "good")]
    tree = LazyIntervalTree(intervals)
    print(tree.intervals)
    tree.merge_intervals(data_combiner=list)
    print(tree.intervals)
