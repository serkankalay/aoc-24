import itertools
import operator
from typing import Callable


def _parse_line(line: str) -> tuple[int, list[int]]:
    elements = line.split(' ')
    return (
        int(elements[0].replace(":", "")),
        [int(i) for i in elements[1:]]
    )


def _parse_input() -> list[tuple[int, list[int]]]:
    with open('input/input_7_1.txt') as file:
        return [
            _parse_line(line.strip())
            for line in file
        ]
    

_CACHED_OPERATIONS = dict()


def concat(first: int, second: int) -> int:
    return int(f"{first}{second}")


def _get_potential_operations(count: int, ops: list[Callable]) -> list[list[Callable]]:
    _CACHED_OPERATIONS.clear()
    if count not in _CACHED_OPERATIONS:
        _CACHED_OPERATIONS[count] = list(itertools.product(ops, repeat=count))
    return _CACHED_OPERATIONS[count]


def _calculate(elements: list[int], c: list[Callable]) -> int:
    iterator = iter(elements)
    total = next(iterator)
    
    for i, element in enumerate(iterator):
        total = c[i](total, element)
    
    return total


def _can_be_feasible(target: int, elements: list[int], ops: list[Callable]) -> bool:
    return any(
        target == _calculate(elements, c)
        for c in _get_potential_operations(len(elements) - 1, ops)
    )
    


if __name__ == '__main__':
    tests = _parse_input()
    print(sum(t[0] for t in list(filter(lambda t: _can_be_feasible(t[0], t[1], [operator.add, operator.mul]), tests))))
    print(sum(t[0] for t in list(filter(lambda t: _can_be_feasible(t[0], t[1], [operator.add, operator.mul, concat]), tests))))
