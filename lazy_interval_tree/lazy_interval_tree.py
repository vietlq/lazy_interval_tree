from collections import namedtuple
from copy import deepcopy
from typing import Any, Callable, Optional, Iterable, List, Set


_Interval = namedtuple("_Interval", "begin,end,data")
_IntervalPoint = namedtuple("_IntervalPoint", "pval,ptype,data")


def set_union(a: Set[Any], b: Set[Any]) -> Set[Any]:
    return a | b


def combine_lists(a: List[Any], b: List[Any]) -> List[Any]:
    return a + b


def extend_list(a: List[Any], b: List[Any]) -> List[Any]:
    a.extend(b)
    return a


class Interval(_Interval):
    """
    Note that creating a new Interval takes 4-5 times longer than a normal tuple
        %timeit tuple([1, 2, "data"])
        149 ns ± 4.27 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
        %timeit Interval(1, 2, "data")
        695 ns ± 14 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

    It takes almost as twice longer to access a named element from Interval than from a normal tuple
        interval_tuple = tuple([1, 2, "data"])
        %timeit interval_tuple[1]
        39.5 ns ± 1.04 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
        interval = Interval(1, 2, "data")
        %timeit interval.end
        60.2 ns ± 3.02 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

    However if we access the elements using numeric index then it is the same with normal tuple
        %timeit interval[1]
        38.9 ns ± 2.73 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
    """

    def __new__(self, begin: Any, end: Any, data: Optional[Any] = None) -> "Interval":
        if begin >= end:
            raise ValueError(f"The `begin` must always be less than `end`! Actual begin={begin} end={end}")
        return super().__new__(self, begin, end, data)


class IntervalPoint(_IntervalPoint):
    pass


class LazyIntervalTree:
    def __init__(self, intervals: Optional[Iterable[Interval]] = None, shallow_copy: bool = True) -> None:
        input_intervals = intervals if intervals else []
        self.intervals = list(input_intervals) if shallow_copy else deepcopy(list(input_intervals))

    def add(self, interval: Interval) -> None:
        self.intervals.append(interval)

    def addi(self, begin: Any, end: Any, data: Optional[Any] = None) -> None:
        self.intervals.append(Interval(begin, end, data))

    def merge_overlaps(self, data_combiner: Callable[[Any, Any], Any] = set_union) -> None:
        """
        Merge overlapping intervals.
        """
        if len(self.intervals) < 2:
            return

        self.intervals = sorted(self.intervals)

        if self.intervals[0].data is not None and data_combiner is None:
            raise ValueError(
                f"Data in the interval {self.intervals[0]} is not `None`!"
                " Expecting `data_combiner` to be a valid calable!"
            )

        result = [self.intervals[0]]

        for interval in self.intervals[1:]:
            if interval.begin < result[-1].end:
                last = result.pop()
                result.append(Interval(last.begin, max(last.end, interval.end), None))

        self.intervals = result

    def split_overlaps(self, data_combiner: Optional[Callable[[Any, Any], Any]] = set_union) -> None:
        """
        Split overlapping intervals and combine data for overlapping cases.
        """
        self.intervals = split_overlaps(self.intervals)

    def split_overlaps_and_merge_data(self, data_combiner: Optional[Callable[[Any, Any], Any]] = None) -> None:
        """
        Split overlapping intervals and then merge newly created sub-intervals.
        """
        pass

    def overlay_on_another_tree(self, tree: "LazyIntervalTree") -> "LazyIntervalTree":
        """
        Overlay on another LazyIntervalTree.
        """
        pass

    def __truediv__(self, rhs: "LazyIntervalTree") -> "LazyIntervalTree":
        """
        Overlay on another LazyIntervalTree. This overloads the division operator `/`.
        """
        return self.overlay_on_another_tree(rhs)


def split_overlaps(
    intervals: Iterable[Interval], data_combiner: Callable[[Any, Any], Any] = set_union
) -> List[Interval]:
    """
    Split overlapping intervals and combine data for overlapping cases.
    """
    points: List[IntervalPoint] = []
    # Note that `intervals` can be a generator, so we defer length check to `points` instead
    for interval in intervals:
        data = interval.data if isinstance(interval.data, set) else {interval.data}
        points.append(IntervalPoint(interval.begin, "L", data))
        points.append(IntervalPoint(interval.end, "R", data))

    if len(points) == 0:
        return []

    points = sorted(points)

    stack: List[IntervalPoint] = [points[0]]
    result: List[Interval] = []

    for point in points[1:]:
        last = stack.pop()
        if last.ptype not in ["L", "R"]:
            raise ValueError(f"Invalid point `last`={last}!")
        if point.ptype not in ["L", "R"]:
            raise ValueError(f"Invalid point `point`={point}!")

        if last.ptype == "L":
            if point.ptype == "L":
                stack.append(IntervalPoint(point.pval, point.ptype, data_combiner(last.data, point.data)))
                if last.pval < point.pval:
                    result.append(Interval(last.pval, point.pval, last.data))
            else:  # point.ptype == "R"
                stack.append(point)
                if last.pval < point.pval:
                    result.append(Interval(last.pval, point.pval, data_combiner(last.data, point.data)))
        else:  # last.ptype == "R"
            if point.ptype == "L":
                stack.append(point)
            else:  # point.ptype == "R"
                stack.append(point)
                if last.pval < point.pval:
                    result.append(Interval(last.pval, point.pval, point.data))

    return result
