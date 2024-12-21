from itertools import pairwise
from typing import Callable


def _parse_reports() -> list[list[int]]:
    with open('input/input_2_1.txt') as file:
        return [
            list(map(int, line.strip().split()))
            for line in file
        ]


def _is_safe(report: list[int]) -> bool:
    
    increasing = report[0] < report[1]
    for first, second in pairwise(report):
        if not (0 < abs(first - second) <= 3):
            return False
        
        if increasing and first > second:
            return False
        
        if not increasing and first < second:
            return False
    
    return True


def _is_safe_with_dampener(report: list[int]) -> bool:
    if _is_safe(report):
        return True
    
    return any(
        _is_safe(report[:i] + report[i + 1:])
        for i in range(len(report))
    )


def _count_safe_reports(
    reports: list[list[int]],
    checker: Callable[[list[int]], bool]
) -> int:
    return sum(checker(r) for r in reports)


if __name__ == '__main__':
    reports = _parse_reports()
    print(_count_safe_reports(reports, _is_safe))
    print(_count_safe_reports(reports, _is_safe_with_dampener))
