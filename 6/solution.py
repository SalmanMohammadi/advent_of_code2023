import functools, operator, time
import math

def get_distance_travelled(time_to_hold:int, race_time:int) -> int:
    assert time_to_hold >= 0 and time_to_hold <= race_time
    return (race_time - time_to_hold) * time_to_hold

def get_record_time(race_time: int, record_distance: int) -> int:
    # we can solve the get_distance_travelled fn for t (it has quadratic form)
    return math.floor((race_time + math.sqrt((race_time**2) - (4 * record_distance))) / 2)

def solve_part_one(inpt: str) -> int:
    race_times = list(map(int, inpt[0].split(": ")[1].strip().split()))
    record_distances = list(map(int, inpt[1].split(": ")[1].strip().split()))
    winning_combinations = []
    for race_time, record_distance in zip(race_times, record_distances):
        max_winning_time = get_record_time(race_time, record_distance)
        winning_combinations.append(max_winning_time - (race_time - max_winning_time) + 1)
    return functools.reduce(operator.mul, winning_combinations)

def solve_part_two(inpt: str) -> int:
    race_time = int(inpt[0].split(": ")[1].replace(" ", ""))
    record_distance = int(inpt[1].split(": ")[1].replace(" ", ""))
    max_winning_time = get_record_time(race_time, record_distance)
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
