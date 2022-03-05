from lazy_interval_tree import Interval, LazyIntervalTree


def test_merge_overlaps():
    intervals = [Interval(3, 10, "hello"), Interval(1, 11, "good")]
    tree = LazyIntervalTree(intervals)
    print(tree.intervals)
    tree.merge_overlaps(data_combiner=list)
    print(tree.intervals)


def test_split_overlaps():
    intervals = [Interval(3, 10, "hello"), Interval(1, 11, "good")]
    tree = LazyIntervalTree(intervals)
    print(tree.intervals)

    def set_union(a, b):
        return a | b

    tree.split_overlaps(data_combiner=set_union)
    print(tree.intervals)
