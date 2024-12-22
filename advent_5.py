import dataclasses
import itertools
import random
from typing import Mapping


@dataclasses.dataclass(frozen=True)
class Rule:
    page: int
    predecessors: set[int]
    successors: set[int]


def _parse() -> tuple[Mapping[int, Rule], list[list[int]]]:
    started_updates = False
    rules: dict[int, Rule] = dict()
    updates: list[list[int]] = list()
    with open('input/input_5_1.txt') as file:
        for line in file:
            line = line.strip()
            if line == "" and not started_updates:
                started_updates = True
                continue
            
            if started_updates:
                updates.append([int(p) for p in line.split(",")])
            else:
                p, s = line.split("|")
                if not (pred := rules.get(int(p))):
                    pred = Rule(
                        page=int(p),
                        predecessors=set(),
                        successors=set(),
                    )
                    rules[int(p)] = pred
                pred.successors.add(int(s))
                
                if not (succ := rules.get(int(s))):
                    succ = Rule(
                        page=int(s),
                        predecessors=set(),
                        successors=set(),
                    )
                    rules[int(s)] = succ
                succ.predecessors.add(int(p))
        
        return rules, updates


def _sum_mid_pages(updates: list[list[int]]) -> int:
    print(updates)
    return sum(
        u[int((len(u) + 1) / 2) - 1]
        for u in updates
    )


def _is_correctly_ordered(u: list[int], rules: Mapping[int, Rule]) -> bool:
    for i, page in enumerate(u):
        if rules[page].successors.intersection(set(u[:i])):
            return False
        elif rules[page].predecessors.intersection(set(u[i+1:])):
            return False
    return True


def _filter_correct_ordered(rules: Mapping[int, Rule], updates: list[list[int]]) -> list[list[int]]:
    return list(
        filter(
            lambda u: _is_correctly_ordered(u, rules),
            updates,
        )
    )


def _filter_incorrect_ordered(rules: Mapping[int, Rule], updates: list[list[int]]) -> list[list[int]]:
    return list(
        itertools.filterfalse(
            lambda u: _is_correctly_ordered(u, rules),
            updates,
        )
    )


def _order(update: list[int], rules: Mapping[int, Rule]) -> list[int]:
    while True:
        ordered = []
        pages = list(update)
        while pages:
            without_pred = [
                i
                for i, page in enumerate(pages)
                if not any(
                    other in rules[page].predecessors
                    for other in itertools.chain(pages[:i], pages[i+1:])
                )
            ]
            ordered.append(
                pages.pop(without_pred[random.randrange(len(without_pred))])
            )
        
        if _is_correctly_ordered(ordered, rules):
            return ordered
        else:
            print(f"Could not correctly order: {update}. Trying again.")


if __name__ == '__main__':
    rules, updates = _parse()
    print(_sum_mid_pages(_filter_correct_ordered(rules, updates)))
    print(_sum_mid_pages(list(map(lambda u: _order(u, rules), _filter_incorrect_ordered(rules, updates)))))
