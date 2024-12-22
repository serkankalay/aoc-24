import enum
from typing import Iterable


def _parse_map() -> list[str]:
    with open('input/input_6_1.txt') as file:
        return [line.strip() for line in file]
    

class Direction(enum.StrEnum):
    Up="^"
    Down="v"
    Left="<"
    Right=">"
    
    
Position = tuple[int, int, Direction]
Cell = tuple[int, int]


def _find_position(map: list[str]) -> Position:
    for i, row in enumerate(map):
        if direction := next((d for d in Direction if d in row), None):
            return i, row.index(direction), direction


def _in_map(map: list[str], position: Position) -> bool:
    return (
        0 <= position[0] < len(map)
        and 0 <= position[1] < len(map[position[0]])
    )


def _valid(position: Position, map: list[str]) -> bool:
    return map[position[0]][position[1]] != "#"


def _rotate(position: Position) -> Position:
    match position[2]:
        case Direction.Up:
            new_dir = Direction.Right
        case Direction.Right:
            new_dir = Direction.Down
        case Direction.Down:
            new_dir = Direction.Left
        case Direction.Left:
            new_dir = Direction.Up
    
    return position[0], position[1], new_dir


def _move(position: Position, map: list[str]) -> Position | None:
    match position[2]:
        case Direction.Up:
            new_position = position[0] - 1, position[1], Direction.Up
        case Direction.Down:
            new_position = position[0] + 1, position[1], Direction.Down
        case Direction.Left:
            new_position = position[0], position[1] - 1, Direction.Left
        case Direction.Right:
            new_position = position[0], position[1] + 1, Direction.Right
    
    if not _in_map(map, new_position):
        return None
    elif _valid(new_position, map):
        return new_position
    else:
        return _move(_rotate(position), map)


def _path_out(map: list[str], position: Position) -> list[Cell]:
    path = list([(position[0], position[1])])
    while True:
        if position := _move(position, map):
            path.append((position[0], position[1]))
        else:
            return path


def _is_circular(map: list[str], position: Position) -> bool:
    path = set([])
    while True:
        if position := _move(position, map):
            if position in path:
                return True
            path.add(position)
        else:
            return False


def _place_obstacle(map: list[str], where: Cell) -> list[str]:
    map_clone = list(map)
    map_clone[where[0]] = f"{map_clone[where[0]][:where[1]]}#{map_clone[where[0]][where[1] + 1:]}"
    return map_clone


def _obstacle_points_for_circle(
    candidates: Iterable[Cell],
    map: list[str],
    position: Position
) -> list[Cell]:
    return list(
        filter(
            lambda c: _is_circular(_place_obstacle(map, c), position),
            candidates,
        )
    )


if __name__ == '__main__':
    map = _parse_map()
    guard_position = _find_position(map)
    path_out = _path_out(map, guard_position)
    print(len(set(path_out)))
    print(len(_obstacle_points_for_circle(set(path_out), map, guard_position)))
