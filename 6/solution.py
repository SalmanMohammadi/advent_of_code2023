import functools, operator, time

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
    n_winning_combinations = 0
    for i in range(race_time):
        if get_distance_travelled(i, race_time) > record:
            n_winning_combinations += 1
    return n_winning_combinations

if __name__ == "__main__":
    with open("test") as f:
        inpt = f.read().split('\n')
        start = time.time()
        res = solve_part_one(inpt)
        end = time.time()
        print(f"Part one solution: {res} taking {(end - start):.7f}")

        start = time.time()
        res = solve_part_two(inpt)
        end = time.time()
        print(f"Part two solution: {res} taking {(end - start):.7f}")
