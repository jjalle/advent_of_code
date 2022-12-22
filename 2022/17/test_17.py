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

PATTERN = r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)'

class Direction(Enum):
    NONE=0
    LEFT=1
    RIGHT=2
    DOWN=3

class Tile(Enum):
    ROCK=0
    AIR=1
    SHAPE=2

def process_line(line: str) -> List[Direction]:
    result = list()
    for char in line:
        if char == '<':
            result.append(Direction.LEFT)
        elif char == '>':
            result.append(Direction.RIGHT)
        else:
            raise RuntimeError(f"Impossible")
    return result

class Shape:
    def __init__(self):
        self.rows: List[List[Tuple[int,int]]] = list()
    def fall(self):
        for idx in range(len(self.rows)):
            row = self.rows[idx]
            new_row = [(x,y-1) for x,y in row]
            self.rows[idx] = new_row
    def shift(self, jet: Direction):
        if jet == Direction.LEFT:
            possible = True
            for row in self.rows:
                for x,y in row:
                    if x == 0:
                        possible = False
                        break
                if not possible:
                    break
            if possible:
                for idx in range(len(self.rows)):
                    row = self.rows[idx]
                    new_row = [(x-1,y) for x,y in row]
                    self.rows[idx] = new_row
        elif jet == Direction.RIGHT:
            possible = True
            for row in self.rows:
                for x,y in row:
                    if x == 6:
                        possible = False
                        break
                if not possible:
                    break
            if possible:
                for idx in range(len(self.rows)):
                    row = self.rows[idx]
                    new_row = [(x+1,y) for x,y in row]
                    self.rows[idx] = new_row
        elif jet == Direction.NONE:
            return
        else:
            raise RuntimeError(f"Impossible")

class FirstShape(Shape):
    def __init__(self, xstart:int, ystart: int):
        super().__init__()
        row = [(xstart, ystart), (xstart + 1, ystart), (xstart + 2, ystart), (xstart + 3, ystart)]
        self.rows.append(row)
    def __repr__(self) -> str:
        x,y = self.rows[0]
        return f"1st:({x},{y})"
    def __str__(self) -> str:
        return self.__repr__()

class SecondShape(Shape):
    def __init__(self, xstart:int, ystart: int):
        super().__init__()
        row0 = [(xstart + 1, ystart)]
        row1 = [(xstart, ystart + 1), (xstart + 1, ystart + 1), (xstart + 2, ystart + 1)]
        row2 = [(xstart + 1, ystart + 2)]
        self.rows.append(row0)
        self.rows.append(row1)
        self.rows.append(row2)
    def __repr__(self) -> str:
        x,y = self.rows[0]
        return f"2nd:({x},{y})"
    def __str__(self) -> str:
        return self.__repr__()

class ThirdShape(Shape):
    def __init__(self, xstart:int, ystart: int):
        super().__init__()
        row0 = [(xstart, ystart), (xstart + 1, ystart), (xstart + 2, ystart)]
        row1 = [(xstart + 2, ystart + 1)]
        row2 = [(xstart + 2, ystart + 2)]
        self.rows.append(row0)
        self.rows.append(row1)
        self.rows.append(row2)
    def __repr__(self) -> str:
        x,y = self.rows[0]
        return f"3rd:({x},{y})"
    def __str__(self) -> str:
        return self.__repr__()

class FourthShape(Shape):
    def __init__(self, xstart:int, ystart: int):
        super().__init__()
        row0 = [(xstart, ystart)]
        row1 = [(xstart, ystart + 1)]
        row2 = [(xstart, ystart + 2)]
        row3 = [(xstart, ystart + 3)]
        self.rows.append(row0)
        self.rows.append(row1)
        self.rows.append(row2)
        self.rows.append(row3)
    def __repr__(self) -> str:
        x,y = self.rows[0]
        return f"4th:({x},{y})"
    def __str__(self) -> str:
        return self.__repr__()

class FifthShape(Shape):
    def __init__(self, xstart:int, ystart: int):
        super().__init__()
        row0 = [(xstart, ystart), (xstart + 1, ystart)]
        row1 = [(xstart, ystart + 1), (xstart + 1, ystart + 1)]
        self.rows.append(row0)
        self.rows.append(row1)
    def __repr__(self) -> str:
        x,y = self.rows[0]
        return f"4th:({x},{y})"
    def __str__(self) -> str:
        return self.__repr__()

class Map:
    def __init__(self, jets: List[Direction]):
        self.steps = 0
        self.tiles = dict()
        self.falling_shape: Shape = None
        self.shape_class = [FirstShape, SecondShape, ThirdShape, FourthShape, FifthShape]
        self.shape_idx = 0
        self.bottom = -1
        self.jets = jets
        self.jet_idx = 0
        self.count = 0
        self.fresh_shape = False
    def get_state_hash(self) -> str:
        rows = list()
        shape = list()
        for row in self.falling_shape.rows:
            for entry in row:
                shape.append(entry)
        key = ''
        for ny in range(100):
            y = self.bottom + 8 - ny
            if y < 0:
                key += "-------"
            else:
                row = list()
                for x in range(7):
                    if (x,y) in shape:
                        key += "@"
                    elif x in self.tiles:
                        if y in self.tiles[x]:
                            val = self.tiles[x][y]
                            if val == Tile.ROCK:
                                key += "#"
                            elif val == Tile.AIR:
                                key += "."
                            elif val == Tile.SHAPE:
                                key += "@"
                        else:
                            key += "."
                    else:
                        key += "."
        key += str(self.shape_idx)
        key += str(self.jet_idx)
        return key
    def get_count(self) -> int:
        return self.count
    def get_height(self) -> int:
        return self.bottom + 1
    def add_shape(self):
        if self.falling_shape is not None:
            raise RuntimeError(f"Impossible")
        self.count += 1
        shape = self.shape_class[self.shape_idx]
        self.shape_idx += 1
        self.shape_idx %= len(self.shape_class)
        x = 2
        y = self.bottom + 4
        self.falling_shape = shape(x, y)
        self.fresh_shape = True
    def collide(self, shape: Shape):
        max_y = self.bottom
        for row in shape.rows:
            for x,y in row:
                if not x in self.tiles:
                    self.tiles[x] = dict()
                self.tiles[x][y] = Tile.ROCK
                if y > max_y:
                    max_y = y
        self.bottom = max_y
    def collision(self, shape: Shape, dir: Direction) -> bool:
        if dir == Direction.RIGHT:
            dx = 1
            dy = 0
        elif dir == Direction.LEFT:
            dx = -1
            dy = 0
        elif dir == Direction.DOWN:
            dx = 0
            dy = -1
        elif dir == Direction.NONE:
            return False
        else:
            raise RuntimeError(f"Impossible")
        for row in shape.rows:
            for x,y in row:
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx > 6:
                    # Collision!
                    return True
                elif ny < 0:
                    # Collision!
                    return True
                elif nx in self.tiles:
                    if ny in self.tiles[nx]:
                        tile = self.tiles[nx][ny]
                        if tile == Tile.ROCK:
                            # Collision!
                            return True
                else:
                    continue
        return False
    def draw(self):
        rows = list()
        ymax = self.bottom
        for y in range(ymax + 8):
            row = list()
            for x in range(7):
                tile = Tile.AIR
                if x in self.tiles:
                    if y in self.tiles[x]:
                        tile = self.tiles[x][y]
                row.append(tile)
            rows.append(row)
        if self.falling_shape:
            for row in self.falling_shape.rows:
                for x,y in row:
                    rows[y][x] = Tile.SHAPE
        rows.reverse()
        lines = list()
        for row in rows:
            line = "|"
            for tile in row:
                if tile == Tile.AIR:
                    col = "."
                elif tile == Tile.ROCK:
                    col = "#"
                elif tile == Tile.SHAPE:
                    col = "@"
                else:
                    raise RuntimeError(f"Impossible")
                line += col
            line += "|"
            lines.append(line)
        lines.append("---------")
        print(f"")
        for line in lines:
            print(line)

    def step(self):
        self.fresh_shape = False
        self.steps += 1
        jet = self.jets[self.jet_idx]
        self.jet_idx += 1
        self.jet_idx %= len(self.jets)
        shape = self.falling_shape
        # Apply jet if not collision
        if not self.collision(shape, jet):
            shape.shift(jet)
        # Fall down or collide
        if self.collision(shape, Direction.DOWN):
            self.collide(shape)
            self.falling_shape = None
            self.add_shape()
        else:
            self.falling_shape.fall()
        return None

def sol1(input_file: Path) -> List[int]:
    jets: List[Direction] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            sjets = process_line(line)
            jets.extend(sjets)
    map = Map(jets)
    map.add_shape()
    map.draw()
    while map.get_count() < 2023:
        map.step()
    height = map.get_height()
    print(f"Result: {height}")

def sol2(input_file: Path) -> List[int]:
    jets: List[Direction] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            sjets = process_line(line)
            jets.extend(sjets)
    map = Map(jets)
    map.add_shape()
    #map.draw()
    memo = dict()
    # Find cycle
    while map.get_count() < 1000000000001:
        map.step()
        if map.fresh_shape:
            key = map.get_state_hash()
            count = map.get_count()
            height = map.get_height()
            if key in memo:
                new = (count, height)
                prev = memo[key]
                prev_count, prev_height = prev
                dcount = count - prev_count
                dheight = height - prev_height
                if (1000000000001 - count) % dcount == 0:
                    # Found answer!
                    result = height + ((1000000000001-count)//dcount)*dheight
                    print(f"Found result: {result}")
                    break
                else:
                    print(f"Found cycle! Count: {count}, Prev: {prev}, New: {new}, DCount: {dcount}, DHeight: {dheight}")
            memo[key] = (count, height)
    height = map.get_height()
    print(f"Result: {height}")

def test_1_test():
    input_file = Path('2022/17/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/17/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/17/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/17/input.txt')
    result = sol2(input_file)
    print(result)