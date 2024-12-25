import dataclasses
import itertools
from collections import defaultdict
from typing import Mapping, Iterator, Callable


@dataclasses.dataclass(frozen=True)
class Direction:
    delta_x: int
    delta_y: int


@dataclasses.dataclass(frozen=True)
class Cell:
    x: int
    y: int
    
    def __add__(self, other: Direction) -> "Cell":
        return Cell(x=self.x + other.delta_x, y=self.y + other.delta_y)
    
    def __sub__(self, other: "Cell") -> Direction:
        return Direction(delta_x=self.x - other.x, delta_y=self.y - other.y)

def _parse_map() -> list[str]:
    with open('input/input_8_1.txt') as file:
        return [line.strip() for line in file]


def _antennas_by_freq(map: list[str]) -> Mapping[str, list[Cell]]:
    mapping: dict[str, list[Cell]] = defaultdict(list)
    
    for x, row in enumerate(map):
        for y, cell_content in enumerate(row):
            if cell_content != ".":
                mapping[cell_content].append(Cell(x, y))
    
    return mapping


def _in_map(map: list[str], cell: Cell) -> bool:
    return (
        0 <= cell.x < len(map)
        and 0 <= cell.y < len(map[cell.x])
    )


def _calculate_antinodes_distance_based(
    zone_map: list[str],
    first: Cell,
    second: Cell,
) -> Iterator[Cell]:
    if (candidate1 := (first + (first - second))) and _in_map(zone_map, candidate1):
        yield candidate1
    
    if (candidate2 := (second + (second - first))) and _in_map(zone_map, candidate2):
        yield candidate2


def _antinode_locations(
    zone_map: list[str],
    cells: list[Cell],
    antinode_calculator: Callable[[list[str], Cell, Cell], Iterator[Cell]],
) -> list[Cell]:
    return list(
        itertools.chain.from_iterable(
            antinode_calculator(zone_map, first, second)
            for first, second in itertools.combinations(cells, 2)
        )
    )
    

def _generate_antinodes(
    zone_map: list[str],
    antennas_by_freq: Mapping[str, list[Cell]],
    antinode_calculator: Callable[[list[str], Cell, Cell], Iterator[Cell]],
) -> list[Cell]:
    return list(
        itertools.chain.from_iterable(
            _antinode_locations(zone_map, cells, antinode_calculator)
            for freq, cells in antennas_by_freq.items()
        )
    )


def _calculate_antinodes_with_resonant_harmonics(
    zone_map: list[str],
    first: Cell,
    second: Cell,
) -> Iterator[Cell]:
    yield first
    yield second
    dist_fwd = first - second
    candidate_fwd = first + dist_fwd
    while _in_map(zone_map, candidate_fwd):
        yield candidate_fwd
        candidate_fwd += dist_fwd
    
    dist_bwd = second - first
    candidate_bwd = second + dist_bwd
    while _in_map(zone_map, candidate_bwd):
        yield candidate_bwd
        candidate_bwd += dist_bwd


if __name__ == '__main__':
    map = _parse_map()
    print(len(set(_generate_antinodes(map, _antennas_by_freq(map), _calculate_antinodes_distance_based))))
    print(len(set(_generate_antinodes(map, _antennas_by_freq(map), _calculate_antinodes_with_resonant_harmonics))))
