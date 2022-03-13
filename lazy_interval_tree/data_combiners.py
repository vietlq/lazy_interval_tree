from typing import Any, List, Set, Dict


def combine_sets(a: Set[Any], b: Set[Any]) -> Set[Any]:
    """
    Returns union of two sets. The order does not matter!
    """
    return a | b


def combine_dicts_to_dict_of_sets(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Set[Any]]:
    """
    Returns union of two dicts. Matching keys will have values pushed into a set. The order does not matter!
    """
    result = {k: {v} for (k, v) in a}
    for k, v in b.items():
        if k in result:
            result[k].add(v)
        else:
            result[k] = {v}
    return result


def combine_lists(a: List[Any], b: List[Any]) -> List[Any]:
    """
    Returns sum of two lists. The order matters a little.
    """
    return a + b


def combine_dicts_to_dict_of_lists(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, List[Any]]:
    """
    Returns union of two dicts. Matching keys will have values pushed into a list. The order matters a little.
    """
    result = {k: [v] for (k, v) in a}
    for k, v in b.items():
        if k in result:
            result[k].append(v)
        else:
            result[k] = [v]
    return result
