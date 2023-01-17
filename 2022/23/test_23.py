import pytest
from typing import Optional, List, Tuple, Set, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict, deque
import re
import json
from enum import Enum
from functools import cmp_to_key
import itertools

DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]
NEIGHBORS = [
    [(-1,-1), (-1,0), (-1,1)],
    [(1,-1), (1,0), (1,1)],
    [(-1,-1), (0,-1), (1,-1)],
    [(-1,1), (0,1), (1,1)]
]

class Map:
    def __init__(self):
        self.elves: List[Tuple[int,int]] = list()
        self.dir_idx: int  = 0
        self.positions: Set[Tuple[int,int]] = set()
        self.destiny: bool = False
    def add_elf(self, pos: Tuple[int,int]):
        self.elves.append(pos)
        self.positions.add(pos)
    def get_rectangle(self) -> Tuple[int,int,int,int]:
        minr = float('inf')
        maxr = 0
        minc = float('inf')
        maxc = 0
        for r,c in self.elves:
            if r > maxr:
                maxr = r
            if r < minr:
                minr = r
            if c > maxc:
                maxc = c
            if c < minc:
                minc = c
        return (minr, maxr, minc, maxc)
    def elf_alone(self, idx: int) -> bool:
        r,c = self.elves[idx]
        adjancent = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dr, dc in adjancent:
            nr, nc = r + dr, c + dc
            if (nr,nc) in self.positions:
                return False
        return True
    def has_no_neighbor(self, idx: int, dir_idx: int) -> bool:
        r,c = self.elves[idx]
        for dr, dc in NEIGHBORS[dir_idx]:
            nr, nc = r + dr, c + dc
            if (nr,nc) in self.positions:
                return False
        return True
    def get_proposed_position(self, idx: int) -> Tuple[int, int]:
        r,c = self.elves[idx]
        if self.elf_alone(idx):
            return (r,c)
        else:
            dir = self.dir_idx
            dr, dc = DIRECTIONS[dir]
            if self.has_no_neighbor(idx, dir):
                return (r+dr,c+dc)
            else:
                dir = (self.dir_idx + 1) % 4
                dr, dc = DIRECTIONS[dir]
                if self.has_no_neighbor(idx, dir):
                    return (r+dr,c+dc)
                else:
                    dir = (self.dir_idx + 2) % 4
                    dr, dc = DIRECTIONS[dir]
                    if self.has_no_neighbor(idx, dir):
                        return (r+dr,c+dc)
                    else:
                        dir = (self.dir_idx + 3) % 4
                        dr, dc = DIRECTIONS[dir]
                        if self.has_no_neighbor(idx, dir):
                            return (r+dr,c+dc)
                        else:
                            return (r,c)
    def get_proposed_positions(self) -> List[Tuple[int,int]]:
        result = list()
        for idx, pos in enumerate(self.elves):
            proposal = self.get_proposed_position(idx)
            result.append(proposal)
        return result
    def move_elves(self, proposed_positions: List[Tuple[int,int]]):
        move = [True for _ in self.elves]
        all_proposed = dict()
        for idx, pos in enumerate(proposed_positions):
            if pos in all_proposed:
                move[idx] = False
                old_idx = all_proposed[pos]
                move[old_idx] = False
            else:
                all_proposed[pos] = idx
        someone_moved = False
        for idx, (allow, pos) in enumerate(zip(move, proposed_positions)):
            if allow:
                old_pos = self.elves[idx]
                if old_pos != pos:
                    self.positions.remove(old_pos)
                    self.elves[idx] = pos
                    self.positions.add(pos)
                    someone_moved = True
        if not someone_moved:
            # Destiny reached
            self.destiny = True
    def round(self):
        ppos = self.get_proposed_positions()
        self.move_elves(ppos)
        self.dir_idx = (self.dir_idx + 1) % 4
    def get_empty_positions(self) -> int:
        minr, maxr, minc, maxc = self.get_rectangle()
        count = 0
        for r in range(minr, maxr + 1):
            for c in range(minc, maxc + 1):
                pos = (r,c)
                if (r,c) in self.positions:
                    continue
                else:
                    count += 1
        return count
    def print(self):
        minr, maxr, minc, maxc = self.get_rectangle()
        rows = list()
        for r in range(minr, maxr + 1):
            row = list()
            for c in range(minc, maxc + 1):
                row.append('.')
            rows.append(row)
        for r,c in self.elves:
            rows[r-minr][c-minc] = '#'
        print("")
        for row in rows:
            row_str = ''.join(row)
            print(row_str)
        print(f"")

def process_line(line: str, r: int, map: Map) -> Map:
    for idx, c in enumerate(line):
        if c == '.':
            continue
        elif c == '#':
            map.add_elf((r,idx))
        else:
            raise RuntimeError(f"Impossible")
    return map

def sol1(input_file: Path) -> List[int]:
    print(f"")
    map = Map()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            process_line(line, idx, map)
    map.print()
    for round in range(0,10):
        map.round()
        print(f"Round {round+1}")
        map.print()
        if map.destiny:
            print(f"Destiny reached at round {round+1}")
            break
    minr, maxr, minc, maxc = map.get_rectangle()
    print(f"N:{minr}, S:{maxr}, W:{minc}, E:{maxc}")
    count = map.get_empty_positions()
    print(f"Result: {count}")

def sol2(input_file: Path) -> List[int]:
    print(f"")
    map = Map()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            process_line(line, idx, map)
    map.print()
    round = 0
    while True:
        map.round()
        if map.destiny:
            print(f"Destiny reached at round {round+1}")
            break
        else:
            round += 1
    print(f"Result: {round+1}")

def test_1_test_small():
    input_file = Path('2022/23/input_test_small.txt')
    result = sol1(input_file)
    print(result)

def test_1_test():
    input_file = Path('2022/23/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/23/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test_small():
    input_file = Path('2022/23/input_test_small.txt')
    result = sol2(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/23/input_test.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/23/input.txt')
    result = sol2(input_file)
    print(result)