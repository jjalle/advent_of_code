import pytest
from typing import Optional, List, Tuple, Set, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict, deque
import re
import json
import copy
from enum import Enum, IntEnum
from functools import cmp_to_key
import itertools
import math

DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]
POSSIBLE_DIRECTIONS = [(0,0), (-1,0), (1,0), (0,-1), (0,1)]
NEIGHBORS = [
    [(-1,-1), (-1,0), (-1,1)],
    [(1,-1), (1,0), (1,1)],
    [(-1,-1), (0,-1), (1,-1)],
    [(-1,1), (0,1), (1,1)]
]

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

class Tile(Enum):
    NONE=0
    WALL=1

class Direction(IntEnum):
    UP=0
    DOWN=1
    LEFT=2
    RIGHT=3

class Map:
    def __init__(self):
        self.grid: List[List[Tile]] = list()
        self.blizzards: List[Tuple[int,int]] = list()
        self.blizzard_directions: List[Direction] = list()
        self.blizzard_grid: List[List[int]] = list()
        self.blizzard_grids: List[List[List[int]]] = list()
        self.r = 0
        self.c = 0
        self.n = 0
        self.start_pos: Tuple[int,int] = (0,1)
        self.end_pos: Tuple[int,int] = (0,1)
    def add_row(self, row: List[Tile]):
        self.grid.append(row)
        brow = [0 for _ in row]
        self.blizzard_grid.append(brow)
    def add_blizzard(self, pos: Tuple[int,int], dir: Direction):
        self.blizzards.append(pos)
        self.blizzard_directions.append(dir)
        r,c = pos
        self.blizzard_grid[r][c] = 1
    def compute_all_blizzard_grids(self):
        wrapr = self.r-2
        wrapc = self.c-2
        self.n = lcm(wrapr,wrapc)
        for i in range(self.n):
            self.update_blizzars()
            grid = copy.deepcopy(self.blizzard_grid)
            self.blizzard_grids.append(grid)
        return
    def update_blizzars(self):
        n = len(self.blizzards)
        for idx in range(0,n):
            r,c = self.blizzards[idx]
            dir = self.blizzard_directions[idx]
            dr, dc = DIRECTIONS[int(dir)]
            nr,nc = r+dr, c+dc
            tile = self.grid[nr][nc]
            if tile == Tile.NONE:
                # Free to move
                self.blizzards[idx] = (nr,nc)
                self.blizzard_grid[r][c] -= 1
                self.blizzard_grid[nr][nc] += 1
            elif tile == Tile.WALL:
                # Warp around
                if dir == Direction.UP:
                    nr, nc = self.r-2, c
                elif dir == Direction.DOWN:
                    nr, nc = 1, c
                elif dir == Direction.LEFT:
                    nr, nc = r, self.c-2
                elif dir == Direction.RIGHT:
                    nr, nc = r, 1
                else:
                    raise RuntimeError(f"Impossible")
                tile = self.grid[nr][nc]
                if tile != Tile.NONE:
                    raise RuntimeError(f"Impossible")
                self.blizzards[idx] = (nr,nc)
                self.blizzard_grid[r][c] -= 1
                self.blizzard_grid[nr][nc] += 1
            else:
                raise RuntimeError(f"Impossible")
    def finish_map(self):
        self.r = len(self.grid)
        self.c = len(self.grid[0])
        self.end_pos = (self.r-1,self.c-2)
    def print(self):
        rows = list()
        for r in self.grid:
            row = list()
            for tile in r:
                if tile == Tile.NONE:
                    row.append('.')
                elif tile == Tile.WALL:
                    row.append('#')
                else:
                    raise RuntimeError(f"Impossible")
            rows.append(row)
        for pos,dir in zip(self.blizzards, self.blizzard_directions):
            r,c = pos
            count = self.blizzard_grid[r][c]
            if count > 1:
                rows[r][c] = str(count)
            elif dir == Direction.UP:
                rows[r][c] = '^'
            elif dir == Direction.DOWN:
                rows[r][c] = 'v'
            elif dir == Direction.LEFT:
                rows[r][c] = '<'
            elif dir == Direction.RIGHT:
                rows[r][c] = '>'
            else:
                raise RuntimeError(f"Impossible")
        print("")
        for row in rows:
            row_str = ''.join(row)
            print(row_str)
        print(f"")
    def print_blizzard(self, idx: int):
        rows = list()
        for r in self.grid:
            row = list()
            for tile in r:
                if tile == Tile.NONE:
                    row.append('.')
                elif tile == Tile.WALL:
                    row.append('#')
                else:
                    raise RuntimeError(f"Impossible")
            rows.append(row)
        grid = self.blizzard_grids[idx]
        for r, row in enumerate(grid):
            for c, count in enumerate(row):
                if count > 0:
                    rows[r][c] = str(count)
        print("")
        for row in rows:
            row_str = ''.join(row)
            print(row_str)
        print(f"")
    def dfs(self, time: int, pos: Tuple[int, int], best_time: int, visited: Dict[Tuple[Tuple[int,int],int], int]) -> int:
        if time > best_time:
            return best_time
        if pos == self.end_pos:
            return time
        state = (time % self.n)
        bgrid = self.blizzard_grids[state]
        r,c = pos
        min_time = best_time
        found = False
        for dr,dc in POSSIBLE_DIRECTIONS:
            nr,nc = r+dr, c+dc
            if nr < 0 or nr >= self.r:
                continue
            if nc < 0 or nc >= self.c:
                continue
            tile = self.grid[nr][nc]
            if tile == Tile.WALL:
                continue
            if bgrid[nr][nc] > 0:
                continue
            ntime = time + 1
            nstate = (state + 1) % self.n
            npos = (nr,nc)
            v = visited.get((npos, nstate))
            if not v or v > ntime:
                visited[(npos,nstate)] = ntime
                result = self.dfs(ntime, npos, min_time, visited)
                found = True
                if result < min_time:
                    min_time = result
        if not found:
            visited[(pos,state)] = 0
        return min_time
    def dijkstra(self, time: int, state: int, start_pos: Tuple[int,int], end_pos: Tuple[int,int]) -> Tuple[int,int]:
        n = self.n
        pos = start_pos
        visited = dict()
        visited[(pos,state)] = 0
        pq = []
        heapq.heappush(pq, (time, (pos, state)))
        while len(pq) > 0:
            time, (pos, state) = heapq.heappop(pq)
            if pos == end_pos:
                return (time, state)
            ntime = time + 1
            nstate = (state + 1) % n
            ngrid = self.blizzard_grids[nstate]
            r,c = pos
            found = False
            for dr,dc in POSSIBLE_DIRECTIONS:
                nr,nc = r+dr, c+dc
                npos = (nr,nc)
                if nr < 0 or nc < 0:
                    continue
                if nr >= self.r or nc >= self.c:
                    continue
                tile = self.grid[nr][nc]
                if tile == Tile.WALL:
                    continue
                if ngrid[nr][nc] > 0:
                    continue
                v = visited.get((npos,nstate))
                if not v or v > ntime:
                    # Worth visiting
                    visited[(npos, nstate)] = ntime
                    heapq.heappush(pq, (ntime, (npos, nstate)))
                    found = True
            if not found:
                # This state is pointless
                visited[(npos, nstate)] = 0
        return (-1,state)



def process_line(line: str, r: int, map: Map) -> Map:
    row = list()
    blizzards = list()
    for idx, c in enumerate(line):
        if c == '.':
            row.append(Tile.NONE)
        elif c == '#':
            row.append(Tile.WALL)
        elif c == '>':
            row.append(Tile.NONE)
            blizzards.append(((r,idx), Direction.RIGHT))
        elif c == '<':
            row.append(Tile.NONE)
            blizzards.append(((r,idx), Direction.LEFT))
        elif c == '^':
            row.append(Tile.NONE)
            blizzards.append(((r,idx), Direction.UP))
        elif c == 'v':
            row.append(Tile.NONE)
            blizzards.append(((r,idx), Direction.DOWN))
        else:
            raise RuntimeError(f"Impossible")
    map.add_row(row)
    for pos, dir in blizzards:
        map.add_blizzard(pos, dir)
    return map

def sol1(input_file: Path) -> List[int]:
    print(f"")
    map = Map()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            process_line(line, idx, map)
    map.finish_map()
    map.compute_all_blizzard_grids()
    #map.print()
    #for i in range(map.n):
    #    map.print_blizzard(i)
    visited = dict()
    #count = map.dfs(0, map.start_pos, float('inf'), visited) # Recursion depth exceeded!
    count, state = map.dijkstra(0,0,map.start_pos, map.end_pos)
    print(f"Result: {count+1}")

def sol2(input_file: Path) -> List[int]:
    print(f"")
    map = Map()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            process_line(line, idx, map)
    map.finish_map()
    map.compute_all_blizzard_grids()
    # First travel
    count, state = map.dijkstra(0,0,map.start_pos, map.end_pos)
    # Second part
    count, state = map.dijkstra(count, state, map.end_pos, map.start_pos)
    # Third part
    count, state = map.dijkstra(count, state, map.start_pos, map.end_pos)
    print(f"Result: {count+1}")

def test_1_test_small():
    input_file = Path('2022/24/input_test_small.txt')
    result = sol1(input_file)
    print(result)

def test_1_test():
    input_file = Path('2022/24/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/24/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/24/input_test.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/24/input.txt')
    result = sol2(input_file)
    print(result)