import itertools
from functools import partial
from typing import Literal


def _parse_matrix() -> tuple[list[str], list[str]]:
    with open('input/input_4_1.txt') as file:
        rows = [line.rstrip() for line in file]
        columns = [""] * len(rows[0])
        for r in rows:
            for i, c in enumerate(r):
                columns[i] += c
        
        return rows, columns


def _count(target: str, word: str) -> int:
    if len(target) < len(word):
        return 0
    return target.startswith(word)


def _extract_diagonal(
    row_direction: Literal["forward", "backward"],
    column_direction: Literal["upward", "downward"],
    cell: tuple[int, int],
    rows: list[str],
    columns: list[str],
) -> str:
    row_iterator = range(
        cell[1],
        len(rows[0]) if row_direction == "forward" else -1,
        1 if row_direction == "forward" else -1,
    )
    column_iterator = range(
        cell[0],
        len(columns[0]) if column_direction == "downward" else -1,
        1 if column_direction == "downward" else -1,
    )
    
    try:
        return str.join("", (rows[c][r] for r,c in zip(row_iterator, column_iterator)))
    except IndexError:
        return ""


def _count_from_cell(
    rows: list[str],
    columns: list[str],
    cell: tuple[int, int],
) -> int:
    row = rows[cell[0]]
    column = columns[cell[1]]
    count = partial(_count, word="XMAS")
    diagonal_word = partial(_extract_diagonal, rows=rows, columns=columns, cell=cell)
    
    return sum(
        [
            count(row[cell[1]:]),  # Forward
            count(row[:cell[1]+1][::-1]),  # Backward
            count(column[cell[0]:]),  # Downward
            count(column[:cell[0]+1][::-1]),  # Upward
            sum(
                count(diagonal_word(r_dir, c_dir))
                for r_dir, c_dir in itertools.product(
                    *[["forward", "backward"], ["upward", "downward"]]
                )
            ),
        ]
        
    )


def _scan_word(rows: list[str], columns: list[str]) -> int:
    return sum(
        _count_from_cell(rows, columns, (x, y))
        for x in range(len(columns))
        for y in range(len(rows))
    )


def _forming_x_mas(
    rows: list[str],
    columns: list[str],
    cell: tuple[int, int],
) -> bool:
    diagonal_word = partial(_extract_diagonal, rows=rows, columns=columns)
    x, y = cell
    # print(cell)
    if any(
        (
            diagonal_word(f_r_dir, f_c_dir, f).startswith("MAS")
            and diagonal_word(s_r_dir, s_c_dir, s).startswith("MAS")
        )
        for (f, f_r_dir, f_c_dir), (s, s_r_dir, s_c_dir) in [
            (((x-1, y-1), "forward", "downward"), ((x-1, y+1), "backward", "downward")),
            (((x-1, y+1), "backward", "downward"), ((x+1, y+1), "backward", "upward")),
            (((x+1, y+1), "backward", "upward"), ((x+1, y-1), "forward", "upward")),
            (((x+1, y-1), "forward", "upward"), ((x-1, y-1), "forward", "downward")),
        ]
    ):
        # print(f"{cell}: TRUE")
        return True
    return False


def _scan_x_word(rows: list[str], columns: list[str]) -> int:
    return sum(
        _forming_x_mas(rows, columns, (x, y))
        for x in range(len(columns))
        for y in range(len(rows))
        if rows[x][y] == "A"
    )


if __name__ == '__main__':
    rows, columns = _parse_matrix()
    print(_scan_word(rows, columns))
    print(_scan_x_word(rows, columns))
