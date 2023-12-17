from typing import List, Tuple
from collections import OrderedDict

def find_map_header(map_ids: List[str], line: str) -> str:
    return next((map_id for map_id in map_ids if map_id in line), False) 

def apply_map(num:int, dest_start:int, source_start:int) -> int:
    return num - (source_start - dest_start)
    
def convert_seed_to_location(seed: int, 
                             conversion_maps: OrderedDict[str, List[int]]) -> int:
    for _, conversion_map in conversion_maps.items():
        for (dest_start, source_start, map_range) in conversion_map:
            if seed >= (source_start + map_range) or seed < source_start:
                continue
            if seed >= source_start and seed < (source_start + map_range):
                seed = apply_map(seed, dest_start, source_start)
                break
    return seed

def convert_seed_range_to_location(seed_start: int, 
                                   seed_end: int, 
                                   conversion_maps: OrderedDict[str, List[int]]) -> List[int]:
    seed_ranges_in = [(seed_start, seed_end)]
    for _, conversion_map in conversion_maps.items():
        seed_ranges_out = []
        for (dest_start, source_start, map_range) in conversion_map:
            seed_range_in_len = len(seed_ranges_in)
            del_idxs = []
            for i in range(seed_range_in_len):
                seed_range_start, seed_range_end = seed_ranges_in[i]
                if seed_range_start >= source_start and seed_range_end < (source_start + map_range):
                    seed_ranges_out.append((apply_map(seed_range_start, dest_start, source_start), 
                                            apply_map(seed_range_end, dest_start, source_start)))
                    del_idxs.append(i)
                elif seed_range_start >= source_start and seed_range_start < (source_start + map_range) and seed_range_end >= (source_start + map_range):
                    seed_ranges_out.append((apply_map(seed_range_start, dest_start, source_start), 
                                            apply_map(source_start + map_range, dest_start, source_start)))
                    del_idxs.append(i)
                    seed_ranges_in.append((source_start + map_range, seed_range_end))
                elif seed_range_start < source_start and seed_range_end < (source_start + map_range) and seed_range_end >= source_start:
                    seed_ranges_out.append((apply_map(source_start, dest_start, source_start), 
                                            apply_map(seed_range_end, dest_start, source_start)))
                    del_idxs.append(i)
                    seed_ranges_in.append((seed_range_start, source_start))
            seed_ranges_in = [x for i, x in enumerate(seed_ranges_in) if i not in del_idxs]
        seed_ranges_in = list(set(seed_ranges_out + seed_ranges_in))
    return seed_ranges_in

if __name__ == "__main__":
    with open("input") as f:
        inpt = f.read()
        map_ids = [
            "seed", 
            "soil", 
            "fertilizer", 
            "water", 
            "light", 
            "temperature", 
            "humidity"
        ]
        conversion_maps = OrderedDict({k: [] for k in map_ids})
        inpt = inpt.split('\n')
        for i, _ in enumerate(inpt[1:], start=1):
            if map_id := find_map_header(map_ids, inpt[i]):
                i += 1 
                while i < len(inpt) and inpt[i]:
                    dest_start, source_start, range_len = inpt[i].strip().split()
                    conversion_maps[map_id].append(tuple(map(int, (dest_start, source_start, range_len))))
                    i += 1

        import time
        start = time.time()
        seeds_list = [convert_seed_to_location(int(seed), conversion_maps) for seed in inpt[0].split(": ")[1].split()]
        end = time.time()
        print(f"Part one: {min(seeds_list)} taking {(end - start):.5f}s")
        
        seeds_list_part_two = [int(x) for x in inpt[0].split(": ")[1].split()]
        seeds_list_part_two = [(seeds_list_part_two[i], seeds_list_part_two[i+1]) for i in range(0, len(seeds_list_part_two)-1, 2)]  
        seeds_list = []
        start = time.time()
        for i, (lower, upper) in enumerate(seeds_list_part_two):
            cur_range = convert_seed_range_to_location(lower, lower+upper, conversion_maps)
            seeds_list.append(min(cur_range, key=lambda x: x[0])[0])
        end = time.time()
        print(f"Part two: {min(seeds_list)} taking {(end - start):.5f}s")