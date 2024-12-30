from collections import Counter, defaultdict
from functools import reduce
from typing import Mapping


def _parse_stones() -> list[str]:
    with open('input/input_11_1.txt') as file:
        for line in file:
            return line.strip().split(' ')
        

def _alter(stone: str) -> list[str]:
    if stone == "0":
        return ["1"]
    else:
        n_digits = len(stone)
        if n_digits % 2 == 0:
            return [
                str(int(stone[:(n_digits // 2)])),
                str(int(stone[(n_digits // 2):])),
            ]
        else:
            return [str(int(stone) * 2024)]
        

def _blink(stones: Mapping[str, int]) -> Mapping[str, int]:
    
    new_values: dict[str, int] = defaultdict(int)
    for stone, count in stones.items():
        for s in _alter(stone):
            new_values[s] += count
    
    return new_values
            

if __name__ == '__main__':
    stones = _parse_stones()
    print(sum(reduce(lambda acc, _: _blink(acc), range(25), Counter(stones)).values()))
    print(sum(reduce(lambda acc, _: _blink(acc), range(75), Counter(stones)).values()))
