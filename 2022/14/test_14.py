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

class Tile(Enum):
    AIR=0
    ROCK=1
    SAND=2
    SOURCE=3

def process_line(line: str) -> list:
    tokens = line.split('->')
    paths = list()
    for token in tokens:
        token = token.strip()
        pos = token.split(',')
        x = int(pos[0])
        y = int(pos[1])
        paths.append((x,y))
    return paths

def draw_map(xmin: int, xmax: int, ymin: int, ymax: int, lastx: int, lasty: int, map: Dict[int, Dict[int, Tile]]):
    print(f"")
    if ymax-ymin > 20:
        ymax = min(ymax, lasty + 10)
        ymin = max(ymin, lasty - 10)
    if xmax-xmin > 20:
        xmax = min(xmax, lastx + 10)
        xmin = max(xmin, lastx - 10)
    for y in range(ymin, ymax + 1):
        msg = ""
        for x in range(xmin, xmax + 1):
            col = map[x][y]
            if col == Tile.AIR:
                msg += '.'
            elif col == Tile.ROCK:
                msg += '#'
            elif col == Tile.SAND:
                msg += 'o'
            elif col == Tile.SOURCE:
                msg += '+'
            else:
                raise RuntimeError(f"Impossible")
        print(msg)

def get_map(paths: List[List[Tuple[int, int]]]):
    map: Dict[Dict[Tile]] = dict()
    xmin, xmax = float('inf'), 0
    ymin, ymax = 0, 0
    map[500] = dict()
    map[500][0] = Tile.SOURCE
    for path in paths:
        for i in range(0, len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            if x2 >= x1:
                xrange = range(x1, x2 + 1)
            else:
                xrange = range(x2, x1 + 1)
            if y2 >= y1:
                yrange = range(y1, y2 + 1)
            else:
                yrange = range(y2, y1 + 1)
            for x in xrange:
                for y in yrange:
                    if not x in map:
                        map[x] = dict()
                    map[x][y] = Tile.ROCK
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
                    if y > ymax:
                        ymax = y
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if not x in map:
                map[x] = dict()
            if not y in map[x]:
                map[x][y] = Tile.AIR
    return map, xmin, xmax, ymin, ymax

def get_limist(paths: List[List[Tuple[int, int]]]) -> Tuple[int,int,int,int]:
    xmin = float('inf')
    xmax = 0
    ymin = 0
    ymax = 0
    for path in paths:
        for x,y in path:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
    return (xmin, xmax, ymin, ymax)

def sol1(input_file: Path) -> List[int]:
    paths = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            path = process_line(line)
            paths.append(path)
    map, xmin, xmax, ymin, ymax = get_map(paths)
    # Drop sand
    count = 0
    abyss = False
    while not abyss:
        count += 1
        falling = True
        x = 500
        y = 0
        while falling:
            falling = False
            for nx,ny in [(x,y+1),(x-1,y+1),(x+1,y+1)]:
                if nx < xmin or nx > xmax or ny > ymax:
                    abyss = True
                    print(f"Result: {count-1}")
                    return
                tile = map[nx][ny]
                if tile == Tile.AIR:
                    falling = True
                    map[x][y] = Tile.AIR
                    map[nx][ny] = Tile.SAND
                    x = nx
                    y = ny
                    break
            #if count == 4:
            #    draw_map(xmin, xmax, ymin, ymax, x, y, map)
        #draw_map(xmin, xmax, ymin, ymax, x, y, map)
        if count % 10 == 0:
            #draw_map(xmin, xmax, ymin, ymax, x, y, map)
            pass
    print(f"Result: {count-1}")

def sol2(input_file: Path) -> List[int]:
    paths = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            path = process_line(line)
            paths.append(path)
    map = list()
    for x in range(185):
        row = list()
        for y in range(1000):
            row.append(Tile.AIR)
        map.append(row)
    # Assign source
    map[0][500] = Tile.SOURCE
    # Assign walls
    xmax = 0
    for path in paths:
        for i in range(0, len(path) - 1):
            y1, x1 = path[i]
            y2, x2 = path[i+1]
            if x2 >= x1:
                xrange = range(x1, x2 + 1)
            else:
                xrange = range(x2, x1 + 1)
            if y2 >= y1:
                yrange = range(y1, y2 + 1)
            else:
                yrange = range(y2, y1 + 1)
            for x in xrange:
                for y in yrange:
                    map[x][y] = Tile.ROCK
                    if x > xmax:
                        xmax = x
    # Assign floor
    xfloor = xmax + 2
    for y in range(1000):
        map[xfloor][y] = Tile.ROCK
    xmax = xfloor
    # Drop sand
    count = 0
    source = False
    while not source:
        count += 1
        falling = True
        x = 0
        y = 500
        while falling:
            falling = False
            for nx,ny in [(x+1,y),(x+1,y-1),(x+1,y+1)]:
                #draw_map(xmin, xmax, ymin, ymax, x, y, map)
                if nx >= xmax:
                    break
                else:
                    tile = map[nx][ny]
                    if tile == Tile.AIR:
                        falling = True
                        x = nx
                        y = ny
                        break
            if not falling:
                map[x][y] = Tile.SAND
                #if x == 500 and y == 0:
                if map[1][499] == map[1][500] == map[1][501] == Tile.SAND:
                    #draw_map(0, 184, 0, 1000, 500, 0, map)
                    source = True
                    print(f"Result {count+1}")
                    break
    print(f"Result: {count+1}")

def test_1_test():
    input_file = Path('2022/14/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/14/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/14/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/14/input.txt')
    result = sol2(input_file)
    print(result)