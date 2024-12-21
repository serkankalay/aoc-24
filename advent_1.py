from collections import Counter


def _parse_lists() -> tuple[list[int], list[int]]:
    first, second = [], []
    with open('input/input_1_1.txt') as file:
        for line in file:
            vals = line.split()
            first.append(int(vals[0]))
            second.append(int(vals[1]))
    return first, second


def _calculate_total_dist(first: list[int], second: list[int]) -> int:
    return sum(
        abs(f - s)
        for f, s in zip(sorted(first), sorted(second))
    )


def _calculate_similarity_score(first: list[int], second: list[int]) -> int:
    c = Counter(second)
    return sum(map(lambda i: i * c[i], first))


if __name__ == '__main__':
    lists = _parse_lists()
    print(_calculate_total_dist(lists[0], lists[1]))
    print(_calculate_similarity_score(lists[0], lists[1]))
