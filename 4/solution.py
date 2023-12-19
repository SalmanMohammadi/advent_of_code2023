import functools
from typing import List, Tuple
import functools
from timeit import timeit

def solve_part_one(file: str) -> Tuple[List[int], List[int]]:
    totals, n_winning_numbers = [], []
    for card in file.split('\n'):
        card = card.split(": ")[1].split(" | ")
        total = 0
        if points := set.intersection(*[set(map(int, x.split())) for x in card]):
            total = functools.reduce(lambda x, _: x * 2,range(1, len(points)+1))
        totals.append(total)
        n_winning_numbers.append(len(points))
    return totals, n_winning_numbers

def solve_part_two(n_winning_numbers: List[int], start_idx, end_idx, total:int = 0):
    for i in range(start_idx, end_idx):
        total += 1
        if n_winning_numbers[i] > 0 and n_winning_numbers[i+1:]:
            total += solve_part_two(n_winning_numbers, i+1, i+n_winning_numbers[i]+1)
    return total

if __name__ == "__main__":
    with open("input", "r") as f:
        file = f.read()
        totals, n_winning_numbers = solve_part_one(file)

        print(f"Part one solution: {sum(totals)} taking {timeit.timeit('solve_part_one(file)', number=1, globals=globals()):.3f}s")
        print(f"Part two solution: {solve_part_two(n_winning_numbers, 0, len(n_winning_numbers))} taking {timeit.timeit('solve_part_two(n_winning_numbers, 0, len(n_winning_numbers))', number=1, globals=globals()):.3f}s")