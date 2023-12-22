from __future__ import annotations
from dataclasses import dataclass
from types import NotImplementedType
from typing import List
import time

ConnectedPositions = tuple[tuple[int, int], ...]
@dataclass
class Tile:
    value: str
    x: int
    y: int

    def __repr__(self) -> str:
        return self.value
    
    def is_pipe(self):
        return self in ["|", "-", "L", "J", "7", "F", "S"]
    
    def get_connected_idxs(self) -> ConnectedPositions:
        x = self.x
        y = self.y
        if self.value == "|":
            return ((x, y + 1), (x, y - 1))
        elif self.value == "-":
            return ((x + 1, y), (x-1,y))
        elif self.value == "L":
            return ((x, y-1), (x+1,y))
        elif self.value == "J":
            return ((x, y-1), (x-1,y))
        elif self.value == "7":
            return ((x, y+1), (x-1,y))
        elif self.value == "F":
            return ((x, y+1), (x+1,y))
        elif self.value == "S":
            return ((x-1, y), 
                    (x+1, y), 
                    (x, y-1), 
                    (x, y+1))
        elif self.value == ".":
            return ((x, y), (x, y))
    
    def __eq__(self, obj: object) -> bool | NotImplementedType: 
        if isinstance(obj, str):
            return self.value == obj
        if not isinstance(obj, Tile):
            return NotImplemented
        return self.value == obj.value and self.x == obj.x and self.y == obj.y
        
class TileGrid:
    def __init__(self, tile_grid: str):
        self.tile_grid = [[Tile(tile, j, i) for j, tile in enumerate(tiles)] for i, tiles in enumerate(tile_grid)]
        self.starting_tile = self.get_starting_tile()
        self.grid_size = (len(self.tile_grid[0]) - 1, len(self.tile_grid) - 1)
        self.starting_tile.value = "|"

    def find_enclosed_tiles(self, loop: List[List[bool]]) -> List[List[bool]]:
        tiles_mask = [[False for _ in tiles] for tiles in self.tile_grid]
        for i in range(len(self.tile_grid)):
            inside_loop = False
            for j in range(len(self.tile_grid[i])):
                if loop[i][j]:
                    if self.tile_grid[i][j] in ["|", "L", "J"]:
                        inside_loop = not inside_loop
                else:
                    tiles_mask[i][j] = inside_loop
        return tiles_mask
    
    def get_starting_tile(self) -> Tile:
        for tiles in self.tile_grid:
            for tile in tiles:
                if tile == "S":
                    return tile
        raise ValueError
        
    def get_loop(self) -> List[Tile]:
        tile = None
        loop = [[False for _ in tiles] for tiles in self.tile_grid]
        loop[self.starting_tile.y][self.starting_tile.x] = True
        for (x, y) in self.starting_tile.get_connected_idxs():
            if self.tile_grid[y][x].is_pipe():
                tile = self.tile_grid[y][x]
                loop[y][x] = True
        previous_tile = self.starting_tile
        while tile != self.starting_tile:
            for (x, y) in tile.get_connected_idxs():
                new_tile = self.tile_grid[y][x]
                if new_tile != previous_tile and new_tile.is_pipe():
                    previous_tile = tile
                    tile = new_tile
                    loop[y][x] = True
                    break
        return loop

    def __repr__(self):
        return "\n".join(["".join(str(tile) for tile in tiles) for tiles in self.tile_grid])
    
if __name__ == "__main__":
    with open("input") as f:
        inpt = f.read().split('\n')
        tile_grid = TileGrid(inpt)

        start = time.time()
        loop = tile_grid.get_loop()
        loop_size = sum(sum(x for x in tiles) for tiles in loop) // 2
        end = time.time()
        print(f"Part one: {loop_size} taking {(end - start):.5f}s")

        start = time.time()
        enclosed_tiles = sum(sum(x for x in tiles) for tiles in tile_grid.find_enclosed_tiles(loop))
        end = time.time()
        print(f"Part two: {enclosed_tiles} taking {(end - start):.5f}s")