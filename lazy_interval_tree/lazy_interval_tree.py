from collections import namedtuple
from copy import deepcopy
from typing import Any, Callable, Optional, Iterable


_Interval = namedtuple("Interval", "begin,end,data")


class Interval(_Interval):
    def __lt__(self, interval: "Interval") -> bool:
        return (self.begin < interval.begin) or (self.begin == interval.begin and self.end < interval.end)

    def __gt__(self, interval: "Interval") -> bool:
        return (self.begin > interval.begin) or (self.begin == interval.begin and self.end > interval.end)


class LazyIntervalTree:
    def __init__(self, intervals: Optional[Iterable[Interval]] = None, give_ownership: bool = False) -> None:
        input_intervals = intervals if intervals else []
        self.intervals = list(input_intervals) if give_ownership else deepcopy(list(input_intervals))

    def merge_intervals(self, data_combiner: Optional[Callable[[Any, Any], Any]] = None) -> None:
        if len(self.intervals) < 2:
            return

        self.intervals = sorted(self.intervals)
        if self.intervals[0] is not None and data_combiner is None:
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
        pass

    def split_and_merge_intervals(self, data_combiner: Optional[Callable[[Any, Any], Any]] = None) -> None:
        pass
