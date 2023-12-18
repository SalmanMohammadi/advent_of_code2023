import functools, operator, time
import math

def get_distance_travelled(time_to_hold:int, race_time:int) -> int:
    assert time_to_hold >= 0 and time_to_hold <= race_time
    return (race_time - time_to_hold) * time_to_hold

def solve_part_one(inpt: str) -> int:
    race_times = list(map(int, inpt[0].split(": ")[1].strip().split()))
    records = list(map(int, inpt[1].split(": ")[1].strip().split()))
    winning_combinations = []
    for race_time, record in zip(race_times, records):
        n_winning_combinations = 0
        for i in range(race_time):
            if get_distance_travelled(i, race_time) > record:
                n_winning_combinations += 1
        winning_combinations.append(n_winning_combinations)
    return functools.reduce(operator.mul, winning_combinations)

def solve_part_two(inpt: str) -> int:
    race_time = int(inpt[0].split(": ")[1].replace(" ", ""))
    record = int(inpt[1].split(": ")[1].replace(" ", ""))

    max_winning_time = None
    # we can solve the get_distance_travelled fn for t (it has quadratic form)
    # using the current record distance, and search from there
    record_time = (race_time + math.sqrt((race_time**2) - (4 * record))) / 2
    for i in range(int(record_time), 0, -1):
        if get_distance_travelled(i, race_time) > record:
            max_winning_time = i
            break
    return max_winning_time - (race_time - max_winning_time) + 1

if __name__ == "__main__":
    with open("input") as f:
        inpt = f.read().split('\n')
        start = time.time()
        res = solve_part_one(inpt)
        end = time.time()
        print(f"Part one solution: {res} taking {(end - start):.7f}s")

        start = time.time()
        res = solve_part_two(inpt)
        end = time.time()
        print(f"Part two solution: {res} taking {(end - start):.7f}s")
