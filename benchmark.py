from typing import Tuple, Any, Union, List
from datetime import datetime
import numpy as np
import pandas as pd
from numpy import random

from intervaltree.intervaltree import Interval, IntervalTree
from lazy_interval_tree import LazyIntervalTree


def rearrange_pair(pair: Tuple[Any, Any]) -> Tuple[Any, Any]:
    first, second = pair
    if first > second:
        return (second, first)
    return pair


def list_to_zip_range(data: List[Any]) -> List[Tuple[Any, Any]]:
    """
    Skip pairs with equal elements.
    """
    zip_res = zip(data[:-1], data[1:])
    result = [rearrange_pair(pair) for pair in zip_res if pair[0] != pair[1]]
    return result


def populate_empty_tree_from_pairs(
    tree: Union[IntervalTree, LazyIntervalTree], pairs: List[Tuple[Any, Any]]
) -> Union[IntervalTree, LazyIntervalTree]:
    start_time = datetime.utcnow()

    for pair in pairs:
        tree.addi(pair[0], pair[1], None)

    end_time = datetime.utcnow()
    elapsed = (end_time - start_time).total_seconds()
    print(f"populate_empty_tree_from_pairs: seconds_elapsed={elapsed} input_size={len(pairs)}")

    return tree


# https://stackoverflow.com/questions/4542892/possible-interview-question-how-to-find-all-overlapping-intervals
# The best solution O(n*log(n)): https://stackoverflow.com/a/9775727
# More: https://www.baeldung.com/cs/finding-all-overlapping-intervals
def run_bench() -> None:
    random.seed(20220305)
    data = random.randint(2**20, size=1_000_000)
    intervals = list_to_zip_range(data)

    slice_instructions = [
        (intervals, 10),
        (intervals, 100),
        (intervals, 1_000),
        (intervals, 10_000),
        (intervals, 20_000),
        (intervals, 100_000),
        (intervals, None),
    ]

    def _run_bench(tree: Union[IntervalTree, LazyIntervalTree]) -> None:
        for an_iterable, slice_size in slice_instructions:
            final_iterable = an_iterable if slice_size is None else an_iterable[:slice_size]
            populate_empty_tree_from_pairs(tree, final_iterable)

            start_time = datetime.utcnow()
            tree.split_overlaps()
            end_time = datetime.utcnow()
            elapsed = (end_time - start_time).total_seconds()
            print(f"split_overlaps: seconds_elapsed={elapsed} input_size={len(final_iterable)}")

    print(f"Starting benchmark for LazyIntervalTree")
    _run_bench(LazyIntervalTree())
    print(f"Finished benchmark for LazyIntervalTree")

    # print(f"Starting benchmark for IntervalTree")
    # _run_bench(IntervalTree())
    # print(f"Finished benchmark for IntervalTree")


if __name__ == "__main__":
    run_bench()
