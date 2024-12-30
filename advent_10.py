import dataclasses
from typing import Iterator, Iterable


def _parse_map() -> list[list[int]]:
    with open('input/input_10_1.txt') as file:
        return [
            [int(c) for c in line.strip()]
            for line in file
        ]
    

@dataclasses.dataclass(frozen=True)
class Cell:
    x: int
    y: int
    v: int
    
    
@dataclasses.dataclass(frozen=True)
class TrailPath:
    cells: list[Cell]
    
    def complete(self) -> bool:
        return self.cells[-1].v == 9
    

@dataclasses.dataclass(frozen=True)
class TrailHead:
    start: Cell
    paths: list[TrailPath]
    
    @property
    def end_points(self) -> Iterable[Cell]:
        return set(p.cells[-1] for p in self.paths)
    
    @property
    def score(self) -> int:
        return len(set((p.cells[-1].x, p.cells[-1].y) for p in self.paths))
    
    @property
    def rating(self) -> int:
        return len(self.paths)


def _valid_neighbors(m: list[list[int]], point: Cell) -> Iterator[Cell]:
    for delta_x, delta_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        try:
            neighbor_x = point.x + delta_x
            neighbor_y = point.y + delta_y
            assert 0 <= neighbor_x < len(m) and 0 <= neighbor_y < len(m[0])
            v_neighbor = m[neighbor_x][neighbor_y]
            if v_neighbor == (point.v + 1):
                yield Cell(neighbor_x, neighbor_y, v_neighbor)
        except AssertionError:
            pass


def _extract_trailheads(m: list[list[int]]) -> list[TrailHead]:
    loose_ends: list[TrailPath] = []
    for x, row in enumerate(m):
        for y, col in enumerate(row):
            if col == 0:
                loose_ends.append(TrailPath(cells=[Cell(x, y, 0)]))
    
    full_paths: list[TrailPath] = []
    
    while loose_ends:
        path = loose_ends.pop()
        point = path.cells[-1]
        for neighbor in _valid_neighbors(m, point):
            new_path = TrailPath(cells=list(path.cells))
            new_path.cells.append(neighbor)
            if new_path.complete():
                full_paths.append(new_path)
            else:
                loose_ends.append(new_path)
    
    trailheads_by_start: dict[tuple[int, int], TrailHead] = {}
    for path in full_paths:
        if th := trailheads_by_start.get((path.cells[0].x, path.cells[0].y)):
            th.paths.append(path)
        else:
            trailheads_by_start[path.cells[0].x, path.cells[0].y] = TrailHead(
                start=path.cells[0],
                paths=[path]
            )
    
    return list(trailheads_by_start.values())


if __name__ == '__main__':
    m = _parse_map()
    print(sum(t.score for t in _extract_trailheads(m)))
    print(sum(t.rating for t in _extract_trailheads(m)))
