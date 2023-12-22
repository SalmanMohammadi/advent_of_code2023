import itertools
from typing import List
def get_row_col_sizes(
        expansion_factor: int, 
        observatory_data: List[List[str]]
        ) -> tuple[List[int], List[int]]:
    row_sizes = [expansion_factor if set(row) == {"."} else 1 for row in observatory_data]
    column_sizes = [1 for _ in observatory_data[0]]
    for j in range(len(observatory_data[0])):
        if set([observatory_data[i][j] for i in range(len(observatory_data))]) == {"."}:
            column_sizes[j] = expansion_factor
    return row_sizes, column_sizes

if __name__ == "__main__":
    with open("input") as f:
        observatory_data = f.read().split('\n')
        galaxy_idxs = []
        for i in range(len(observatory_data[0])):
            for j in range(len(observatory_data[i])):
                if observatory_data[i][j] == "#":
                    galaxy_idxs.append((i, j))
        galaxy_combinations = list(itertools.combinations(galaxy_idxs, 2))
        row_sizes_2x, column_sizes_2x = get_row_col_sizes(2, observatory_data)
        paths_total_2x = 0

        row_sizes_milx, column_sizes_milx = get_row_col_sizes(1000000, observatory_data)
        paths_total_milx = 0

        for (galaxy_1_idx, galaxy_2_idx) in galaxy_combinations:
            distance_row = sum([row_sizes_2x[galaxy_1_idx[0] + x] for x in range(0, galaxy_2_idx[0] - galaxy_1_idx[0], 1 if galaxy_2_idx[0] > galaxy_1_idx[0] else -1)])
            distance_col = sum([column_sizes_2x[galaxy_1_idx[1] + x] for x in range(0, galaxy_2_idx[1] - galaxy_1_idx[1], 1 if galaxy_2_idx[1] > galaxy_1_idx[1] else -1)])
            paths_total_2x += (distance_col + distance_row)


            distance_row = sum([row_sizes_milx[galaxy_1_idx[0] + x] for x in range(0, galaxy_2_idx[0] - galaxy_1_idx[0], 1 if galaxy_2_idx[0] > galaxy_1_idx[0] else -1)])
            distance_col = sum([column_sizes_milx[galaxy_1_idx[1] + x] for x in range(0, galaxy_2_idx[1] - galaxy_1_idx[1], 1 if galaxy_2_idx[1] > galaxy_1_idx[1] else -1)])
            paths_total_milx += (distance_col + distance_row)

        print(f"Part one: {paths_total_2x}")
        print(f"Part two: {paths_total_milx}")

