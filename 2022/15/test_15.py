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

PATTERN = r'Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
class Tile(Enum):
    AIR=0
    BEACON=1
    SENSOR=2
    IMPOSSIBLE=3

def process_line(line: str) -> Tuple[Tuple[int,int], Tuple[int,int], int, int, int]:
    match = re.match(PATTERN, line)
    if not match:
        raise RuntimeError(f"Impossible")
    sx = int(match.group(1))
    sy = int(match.group(2))
    bx = int(match.group(3))
    by = int(match.group(4))
    md = abs(sx-bx) + abs(sy-by)
    mdx = abs(sx-bx)
    mdy = abs(sy-by)
    return (sx,sy), (bx,by), md, mdx, mdy

def draw_map(xmin: int, xmax: int, ymin: int, ymax: int, lastx: int, lasty: int, map: Dict[int, Dict[int, Tile]]):
    print(f"")
    if ymax-ymin > 50:
        ymax = min(ymax, lasty + 25)
        ymin = max(ymin, lasty - 25)
    if xmax-xmin > 50:
        xmax = min(xmax, lastx + 25)
        xmin = max(xmin, lastx - 25)
    # Print header
    digits = list()
    for x in range(xmin, xmax + 1):
        if x < 0:
            x = -x
            cent = '-'
        else:
            cent = x // 100
        dec = (x % 100) // 10
        uni = (x % 10)
        digits.append((cent, dec, uni))
    cents = [str(cent) for cent, dec, uni in digits]
    decs = [str(dec) for cent, dec, uni in digits]
    unis = [str(uni) for cent, dec, uni in digits]
    print('   ' + ''.join(cents))
    print('   ' + ''.join(decs))
    print('   ' + ''.join(unis))
    for y in range(ymin, ymax + 1):
        cent = y // 100
        dec = (y % 100) // 10
        uni = (y % 10)
        msg = str(cent) + str(dec) + str(uni)
        for x in range(xmin, xmax + 1):
            if not x in map:
                col = Tile.AIR
            elif not y in map[x]:
                col = Tile.AIR
            else:
                col = map[x][y]
            if col == Tile.AIR:
                msg += '.'
            elif col == Tile.BEACON:
                msg += 'B'
            elif col == Tile.SENSOR:
                msg += 'S'
            elif col == Tile.IMPOSSIBLE:
                msg += '#'
            else:
                raise RuntimeError(f"Impossible")
        print(msg)

def sol1_opt(input_file: Path, ycheck: int) -> List[int]:
    paths = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            sensor, beacon, md, mdx, mdy = process_line(line)
            paths.append((sensor, beacon, md))
    # Find max x,y:
    xmin, xmax = float('inf'), 0
    ymin, ymax = float('inf'), 0
    for sensor, beacon, md in paths:
        for x,y in [sensor, beacon]:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
    map = OrderedDict()
    for x in range(xmin, xmax + 1):
        map[x] = OrderedDict()
        for y in range(ycheck - 1, ycheck + 2):
            map[x][y] = Tile.AIR
    for sensor, beacon, md in paths:
        sx, sy = sensor
        bx, by = beacon
        if not sx in map:
            map[sx] = OrderedDict()
        if not bx in map:
            map[bx] = OrderedDict()
        map[sx][sy] = Tile.SENSOR
        map[bx][by] = Tile.BEACON
    possible_blockers = list()
    max_md = 0
    xmin = float('inf')
    xmax = 0
    for yref in range(ycheck - 1, ycheck + 2):
        for sensor, beacon, md in paths:
            sx, sy = sensor
            bx, by = beacon
            mdyref = abs(sy-yref)
            if mdyref <= md:
                possible_blockers.append((sensor, beacon, md))
                if md > max_md:
                    max_md = md
                lx = sx - md
                hx = sx + md
                if lx < xmin:
                    xmin = lx
                if hx > xmax:
                    xmax = hx
    for x in range(xmin, xmax + 1):
        for y in range(ycheck - 1, ycheck + 2):
            for sensor, beacon, md in paths:
                sx, sy = sensor
                bx, by = beacon
                curr_md = abs(sy-y) + abs(sx-x)
                if curr_md <= md:
                    if not x in map:
                        map[x] = OrderedDict()
                    if not y in map[x]:
                        map[x][y] = Tile.AIR
                    tile = map[x][y]
                    if tile == Tile.AIR:
                        map[x][y] = Tile.IMPOSSIBLE
    count = 0
    for x, row in map.items():
        if ycheck in row:
            tile = row[ycheck]
            if tile == Tile.IMPOSSIBLE:
                count += 1
    draw_map(xmin, xmax, ycheck-1, ycheck+1, xmin, ycheck, map)
    print(f"Result: {count}")

def sol2(input_file: Path, ycheck: int) -> List[int]:
    paths = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            sensor, beacon, md, mdx, mdy = process_line(line)
            paths.append((sensor, beacon, md, mdx, mdy))
    # Distress must be right outside a sensor boundary
    xmin, xmax = 0, ycheck
    ymin, ymax = 0, ycheck
    for sensor, beacon, smd, smdx, smdy in paths:
        sx, sy = sensor
        for dx in range(0, smd + 2):
            # Point must be a md + 1 from sx, sy
            dy = smd + 1 - dx
            for x,y in [(sx+dx,sy+dy), (sx-dx,sy+dy), (sx+dx,sy-dy), (sx-dx,sy-dy)]:
                if x < xmin or x > xmax or y < ymin or y > ymax:
                    continue
                found = True
                for osensor, obeacon, omd, omdx, omdy in paths:
                    if osensor == sensor:
                        continue
                    osx, osy = osensor
                    mdx = abs(osx-x)
                    mdy = abs(osy-y)
                    md = mdx + mdy
                    if md <= omd:
                        found = False
                        break
                if found:
                    print(f"Result: x:{x}, y:{y}")
                    count = 4000000*x + y
                    print(f"Count: {count}")
                    return
    print(f"Not found")


def test_1_test():
    input_file = Path('2022/15/test_input.txt')
    result = sol1_opt(input_file, 10)
    print(result)

def test_1():
    input_file = Path('2022/15/input.txt')
    result = sol1_opt(input_file, 2000000)
    print(result)

def test_2_test():
    input_file = Path('2022/15/test_input.txt')
    result = sol2(input_file, 20)
    print(result)

def test_2():
    input_file = Path('2022/15/input.txt')
    result = sol2(input_file, 4000000)
    print(result)