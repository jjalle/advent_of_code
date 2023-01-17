import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict, deque
import re
import json
from enum import Enum
from functools import cmp_to_key
import itertools

class Tile(Enum):
    NONE=0
    OPEN=1
    WALL=2

class Direction(Enum):
    UP=0
    DOWN=1
    RIGHT=2
    LEFT=3

class Rotate(Enum):
    LEFT=0
    RIGHT=1

class Command:
    def __init__(self):
        pass
    def is_rotate(self) -> bool:
        return False
    def is_count(self) -> bool:
        return False
    def get_count(self) -> int:
        raise RuntimeError(f"Impossible")
    def rotate(self, direction: Direction) -> Direction:
        raise RuntimeError(f"Impossible")

class RotateCommand(Command):
    def __init__(self, rot: Rotate):
        super().__init__()
        self.rot_dir = rot
    def is_rotate(self) -> bool:
        return True
    def rotate_right(self, dir: Direction) -> Direction:
        if dir == Direction.UP:
            return Direction.RIGHT
        elif dir == Direction.DOWN:
            return Direction.LEFT
        elif dir == Direction.RIGHT:
            return Direction.DOWN
        elif dir == Direction.LEFT:
            return Direction.UP
        else:
            raise RuntimeError(f"Impossible")
    def rotate_left(self, dir: Direction) -> Direction:
        if dir == Direction.UP:
            return Direction.LEFT
        elif dir == Direction.DOWN:
            return Direction.RIGHT
        elif dir == Direction.RIGHT:
            return Direction.UP
        elif dir == Direction.LEFT:
            return Direction.DOWN
        else:
            raise RuntimeError(f"Impossible")
    def rotate(self, direction: Direction) -> Direction:
        if self.rot_dir == Rotate.LEFT:
            return self.rotate_left(direction)
        elif self.rot_dir == Rotate.RIGHT:
            return self.rotate_right(direction)
        else:
            raise RuntimeError(f"Impossible")
    def __repr__(self) -> str:
        if self.rot_dir == Rotate.RIGHT:
            return f"R"
        elif self.rot_dir == Rotate.LEFT:
            return f"L"
        else:
            raise RuntimeError(f"Impossible")

class CountCommand(Command):
    def __init__(self, count: int):
        super().__init__()
        self.count = count
    def is_count(self) -> bool:
        return True
    def __repr__(self) -> str:
        return f"{self.count}"
    def get_count(self) -> int:
        return self.count

class Map:
    def __init__(self):
        self.rows: List[List[Tile]] = list()
        self.min_col_edges: List[int] = list()
        self.max_col_edges: List[int] = list()
        self.min_row_edges: List[int] = list()
        self.max_row_edges: List[int] = list()
        self.r = 0
        self.c = 0
        self.cursor: Tuple[int,int] = (0,0)
        self.facing: Direction = Direction.RIGHT
        self.path: Dict[Tuple[int,int], str] = dict()
        self.warp: Dict[Tuple[int,int, Direction], Tuple[int,int, Direction]] = dict()
    def add_row(self, row: List[Tile], min: int, max: int):
        self.rows.append(row)
        self.min_col_edges.append(min)
        self.max_col_edges.append(max)
        print(f"Added row min: {min}, max: {max}")
    def finish_map(self):
        self.r = len(self.rows)
        self.cursor = (0, self.min_col_edges[0])
        # Make all rows same length
        maxcols = 0
        for row in self.rows:
            if len(row) > maxcols:
                maxcols = len(row)
        self.c = maxcols
        for row in self.rows:
            missing_cols = self.c - len(row)
            for i in range(0, missing_cols):
                row.append(Tile.NONE)
        self.path[self.cursor] = ">"
        for c in range(0, self.c):
            minr = 0
            maxr = self.r - 1
            start_map = False
            for r in range(0, self.r):
                row = self.rows[r]
                tile = row[c]
                if tile == Tile.NONE:
                    if start_map:
                        start_map = False
                        maxr = r - 1
                elif tile == Tile.OPEN or tile == Tile.WALL:
                    if not start_map:
                        start_map = True
                        minr = r
                else:
                    raise RuntimeError(f"Impossible")
            print(f"For column {c} min: {minr}, maxr: {maxr}")
            self.max_row_edges.append(maxr)
            self.min_row_edges.append(minr)
        # Warp points
        for r in range(self.r):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (r,max,Direction.LEFT)
            self.warp[maxpos] = (r,min,Direction.RIGHT)
        for c in range(self.c):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (max,c, Direction.UP)
            self.warp[maxpos] = (min,c, Direction.DOWN)
    def cube_warping_test(self):
        for r in range(4):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (5,4+r,Direction.DOWN)
            self.warp[maxpos] = (11-r,15,Direction.LEFT)
        for r in range(4,8):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (11,19-r,Direction.UP)
            self.warp[maxpos] = (8,19-r,Direction.DOWN)
        for r in range(8,12):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (7,15-r,Direction.UP)
            self.warp[maxpos] = (11-r,11,Direction.LEFT)
        for c in range(4):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (0,11-c,Direction.DOWN)
            self.warp[maxpos] = (11,11-c,Direction.UP)
        for c in range(4,8):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (c-4,8,Direction.RIGHT)
            self.warp[maxpos] = (15-c,8,Direction.RIGHT)
        for c in range(8,12):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (4,11-c,Direction.DOWN)
            self.warp[maxpos] = (7,11-c,Direction.UP)
        for c in range(12,16):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (19-c,11,Direction.LEFT)
            self.warp[maxpos] = (19-c,0,Direction.RIGHT)
    def cube_warping(self):
        for r in range(50):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (149-r,0,Direction.RIGHT) #OK
            self.warp[maxpos] = (149-r,99,Direction.LEFT) #OK
        for r in range(50,100):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (100,r-50,Direction.DOWN) #OK
            self.warp[maxpos] = (49,50+r,Direction.UP) #OK
        for r in range(100,150):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (149-r,50,Direction.RIGHT) #OK
            self.warp[maxpos] = (149-r,149,Direction.LEFT) #OK
        for r in range(150,200):
            min = self.min_col_edges[r]
            max = self.max_col_edges[r]
            minpos = (r, min, Direction.LEFT)
            maxpos = (r, max, Direction.RIGHT)
            self.warp[minpos] = (0,r-100,Direction.DOWN) #OK
            self.warp[maxpos] = (149,r-100,Direction.UP) #OK
        for c in range(50):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (50+c,50,Direction.RIGHT) #OK
            self.warp[maxpos] = (0,100+c,Direction.DOWN) #OK
        for c in range(50,100):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (100+c,0,Direction.RIGHT) #OK
            self.warp[maxpos] = (100+c,49,Direction.LEFT) #OK
        for c in range(100,150):
            min = self.min_row_edges[c]
            max = self.max_row_edges[c]
            minpos = (min, c, Direction.UP)
            maxpos = (max, c, Direction.DOWN)
            self.warp[minpos] = (199,c-100,Direction.UP) #OK
            self.warp[maxpos] = (c-50,99,Direction.LEFT) #OK
    def get_tile(self, row_idx: int, col_idx: int) -> Tile:
        row = self.rows[row_idx]
        tile = row[col_idx]
        return tile
    def rotate_right(self):
        dir = self.facing
        if dir == Direction.UP:
            self.facing = Direction.RIGHT
        elif dir == Direction.DOWN:
            self.facing = Direction.LEFT
        elif dir == Direction.RIGHT:
            self.facing = Direction.DOWN
        elif dir == Direction.LEFT:
            self.facing = Direction.UP
        else:
            raise RuntimeError(f"Impossible")
    def rotate_left(self):
        dir = self.facing
        if dir == Direction.UP:
            self.facing = Direction.LEFT
        elif dir == Direction.DOWN:
            self.facing = Direction.RIGHT
        elif dir == Direction.RIGHT:
            self.facing = Direction.UP
        elif dir == Direction.LEFT:
            self.facing = Direction.DOWN
        else:
            raise RuntimeError(f"Impossible")
    def move_cursor(self, command: Command) -> Tuple[int, int]:
        if command.is_rotate():
            self.facing = command.rotate(self.facing)
            return self.cursor
        elif not command.is_count():
            raise RuntimeError(f"Impossible")
        direction: Direction = self.facing
        total = command.get_count()
        r, c = self.cursor
        count = 0
        dr, dc = 0,0
        dir_str = ""
        if direction == Direction.UP:
            dr = -1
            dir_str = "^"
        elif direction == Direction.DOWN:
            dr = 1
            dir_str = "v"
        elif direction == Direction.RIGHT:
            dc = 1
            dir_str = ">"
        elif direction == Direction.LEFT:
            dc = -1
            dir_str = "<"
        else:
            raise RuntimeError(f"Impossible")
        self.path[(r,c)] = dir_str
        while count < total:
            nr = r + dr
            nc = c + dc
            if nr < self.min_row_edges[c] or nc < self.min_col_edges[r] or nr > self.max_row_edges[c] or nc > self.max_col_edges[r]:
                # Warping!
                nr, nc, ndirection = self.warp[(r,c,direction)]
                ntile = self.rows[nr][nc]
                if ntile == Tile.WALL:
                    break
                elif ntile == Tile.NONE:
                    raise RuntimeError(f"Bad warping from ({r},{c},{direction}) to ({nr},{nc},{ndirection})")
                elif ntile == Tile.OPEN:
                    # Advance cursor
                    r = nr
                    c = nc
                    direction = ndirection
                    if direction == Direction.UP:
                        dr = -1
                        dc = 0
                        dir_str = "^"
                    elif direction == Direction.DOWN:
                        dr = 1
                        dc = 0
                        dir_str = "v"
                    elif direction == Direction.RIGHT:
                        dr = 0
                        dc = 1
                        dir_str = ">"
                    elif direction == Direction.LEFT:
                        dr = 0
                        dc = -1
                        dir_str = "<"
                    else:
                        raise RuntimeError(f"Impossible")
                    self.path[(r,c)] = dir_str
                    count += 1
            else:
                nrow = self.rows[nr]
                ntile = nrow[nc]
                if ntile == Tile.WALL:
                    # Blocked by wall
                    break
                elif ntile == Tile.NONE:
                    raise RuntimeError(f"Impossible")
                else:
                    # Advance cursor
                    r = nr
                    c = nc
                    self.path[(r,c)] = dir_str
                    count += 1
        self.cursor = (r,c)
        self.facing = direction
        return self.cursor
    def print(self):
        print("")
        for r, row in enumerate(self.rows):
            row_str = ""
            for c, tile in enumerate(row):
                if (r,c) in self.path:
                    val = self.path[(r,c)]
                else:
                    if tile == Tile.NONE:
                        val = " "
                    elif tile == Tile.OPEN:
                        val = "."
                    elif tile == Tile.WALL:
                        val = "#"
                    else:
                        raise RuntimeError(f"Impossible")
                row_str += val
            print(row_str)
        print(f"")

def process_line(line: str, map: Map) -> Map:
    row: List[Tile] = list()
    min_idx = 0
    max_idx = float('inf')
    map_started = False
    for idx, c in enumerate(line):
        if c == ' ':
            if map_started:
                max_idx = idx - 1
                map_started = False
            row.append(Tile.NONE)
        elif c == '.':
            if not map_started:
                min_idx = idx
                map_started = True
            row.append(Tile.OPEN)
        elif c == '#':
            if not map_started:
                min_idx = idx
                map_started = True
            row.append(Tile.WALL)
        elif c == "\n":
            if map_started:
                max_idx = idx - 1
                map_started = False
        else:
            raise RuntimeError(f"Impossible")
    map.add_row(row, min_idx, max_idx)
    return map

def process_ins(line: str, start_dir: Direction) -> List[Command]:
    dir = start_dir
    num_str = ""
    result: List[Command] = list()
    for c in line:
        if c.isalpha():
            num = int(num_str)
            cmd = CountCommand(num)
            num_str = ""
            result.append(cmd)
            if c == "R":
                cmd = RotateCommand(Rotate.RIGHT)
                result.append(cmd)
            elif c == "L":
                cmd = RotateCommand(Rotate.LEFT)
                result.append(cmd)
            else:
                raise RuntimeError(f"Impossible")
        else:
            num_str += c
    num = int(num_str)
    cmd = CountCommand(num)
    num_str = ""
    result.append(cmd)
    return result

def sol1(input_file: Path) -> List[int]:
    print(f"")
    map = Map()
    start_dir = Direction.RIGHT
    path = None
    parsing_map = True
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            strip_line = line.strip()
            if parsing_map:
                if strip_line:
                    process_line(line, map)
                else:
                    parsing_map = False
            else:
                path = process_ins(line, start_dir)
    map.finish_map()
    for ins in path:
        map.move_cursor(ins)
    map.print()
    row, col = map.cursor
    dir = None
    if map.facing == Direction.UP:
        dir = 3
    elif map.facing == Direction.DOWN:
        dir = 1
    elif map.facing == Direction.RIGHT:
        dir = 0
    elif map.facing == Direction.LEFT:
        dir = 2
    else:
        raise RuntimeError(f"Impossible")
    print(f"R:{row+1}, C:{col+1}, F:{dir}")
    result = 1000 * (row + 1) + 4 * (col + 1) + dir
    print(f"Result: {result}")

def sol2(input_file: Path, test: bool) -> List[int]:
    print(f"")
    map = Map()
    start_dir = Direction.RIGHT
    path = None
    parsing_map = True
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            strip_line = line.strip()
            if parsing_map:
                if strip_line:
                    process_line(line, map)
                else:
                    parsing_map = False
            else:
                path = process_ins(line, start_dir)
    map.finish_map()
    if test:
        map.cube_warping_test()
    else:
        map.cube_warping()
    for ins in path:
        map.move_cursor(ins)
    map.print()
    row, col = map.cursor
    dir = None
    if map.facing == Direction.UP:
        dir = 3
    elif map.facing == Direction.DOWN:
        dir = 1
    elif map.facing == Direction.RIGHT:
        dir = 0
    elif map.facing == Direction.LEFT:
        dir = 2
    else:
        raise RuntimeError(f"Impossible")
    print(f"R:{row+1}, C:{col+1}, F:{dir}")
    result = 1000 * (row + 1) + 4 * (col + 1) + dir
    print(f"Result: {result}")

def test_1_test():
    input_file = Path('2022/22/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/22/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/22/input_test.txt')
    result = sol2(input_file, True)
    print(result)

def test_2():
    input_file = Path('2022/22/input.txt')
    result = sol2(input_file, False)
    print(result)