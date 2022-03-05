from collections import namedtuple
from copy import deepcopy
from typing import Any, Callable, Optional, Iterable, List


_Interval = namedtuple("Interval", "begin,end,data")
_IntervalPoint = namedtuple("IntervalPoint", "pval,ptype,data")


class Interval(_Interval):
    def __lt__(self, interval: "Interval") -> bool:
        return (self.begin < interval.begin) or (self.begin == interval.begin and self.end < interval.end)

    def __gt__(self, interval: "Interval") -> bool:
        return (self.begin > interval.begin) or (self.begin == interval.begin and self.end > interval.end)


class IntervalPoint(_IntervalPoint):
    def __lt__(self, point: "IntervalPoint") -> bool:
        return (self.pval < point.pval) or (self.pval == point.pval and self.ptype < point.ptype)

    def __gt__(self, point: "Interval") -> bool:
        return (self.pval > point.pval) or (self.pval == point.pval and self.ptype > point.ptype)


class LazyIntervalTree:
    def __init__(self, intervals: Optional[Iterable[Interval]] = None, shallow_copy: bool = True) -> None:
        input_intervals = intervals if intervals else []
        self.intervals = list(input_intervals) if shallow_copy else deepcopy(list(input_intervals))

    def merge_intervals(self, data_combiner: Optional[Callable[[Any, Any], Any]] = None) -> None:
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

    def split_intervals(self, data_combiner: Optional[Callable[[Any, Any], Any]] = None) -> None:
        """
        Split overlapping intervals and combine data for overlapping cases.
        """
        if len(self.intervals) < 2:
            return

        start_points = []
        end_points = []
        for interval in self.intervals:
            start_points.append(IntervalPoint(interval.begin, "L", {interval.data}))
            end_points.append(IntervalPoint(interval.end, "R", {interval.data}))
        points: List[IntervalPoint] = sorted(start_points + end_points)
        print(f"points={points}")

        stack: List[IntervalPoint] = [points[0]]
        result: List[Interval] = []

        for point in points[1:]:
            if stack[-1].ptype == "L":
                if point.ptype == "L":
                    last = stack.pop()
                    result.append(Interval(last.pval, point.pval, last.data))
                    stack.append(IntervalPoint(point.pval, point.ptype, data_combiner(last.data, point.data)))
                elif point.ptype == "R":
                    last = stack.pop()
                    result.append(Interval(last.pval, point.pval, data_combiner(last.data, point.data)))
                    stack.append(point)
                else:
                    raise ValueError(f"Invalid point {point}!")
            elif stack[-1].ptype == "R":
                if point.ptype == "L":
                    stack.pop()
                elif point.ptype == "R":
                    last = stack.pop()
                    result.append(Interval(last.pval, point.pval, point.data))
                    stack.append(point)
                else:
                    raise ValueError(f"Invalid point {point}!")
            else:
                raise ValueError(f"Invalid point {stack[-1]}!")

        self.intervals = result

    def split_and_merge_intervals(self, data_combiner: Optional[Callable[[Any, Any], Any]] = None) -> None:
        """
        Split overlapping intervals and then merge newly created sub-intervals.
        """
        pass
