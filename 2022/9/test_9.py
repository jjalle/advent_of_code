import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict
import re

def process_input(line: str) -> Tuple[str, int]:
    line = line.strip()
    tokens = line.split(' ')
    dir = tokens[0]
    steps = int(tokens[1])
    return dir, steps

def next_tail(xh, yh, xt, yt) -> Tuple[int, int]:
    if xh == xt:
        if yh == yt:
            return xt, yt
        elif yh > yt:
            diffy = yh - yt
            if diffy > 1:
                yt += 1
                return xt, yt
            else:
                return xt, yt
        else:
            diffy = yt - yh
            if diffy > 1:
                yt -= 1
                return xt, yt
            else:
                return xt, yt
    elif xh > xt:
        diffx = xh - xt
        if yh == yt:
            if diffx > 1:
                xt += 1
                return xt, yt
            else:
                return xt, yt
        elif yh > yt:
            diffy = yh - yt
            if diffy > 1:
                yt += 1
                xt += 1
                return xt, yt
            elif diffx > 1:
                yt += 1
                xt += 1
                return xt, yt
            else:
                return xt, yt
        else:
            diffy = yt - yh
            if diffy > 1:
                yt -= 1
                xt += 1
                return xt, yt
            elif diffx > 1:
                yt -= 1
                xt += 1
                return xt, yt
            else:
                return xt, yt
    else:
        diffx = xt - xh
        if yh == yt:
            if diffx > 1:
                xt -= 1
                return xt, yt
            else:
                return xt, yt
        elif yh > yt:
            diffy = yh - yt
            if diffy > 1:
                yt += 1
                xt -= 1
                return xt, yt
            elif diffx > 1:
                yt += 1
                xt -= 1
                return xt, yt
            else:
                return xt, yt
        else:
            diffy = yt - yh
            if diffy > 1:
                yt -= 1
                xt -= 1
                return xt, yt
            elif diffx > 1:
                yt -= 1
                xt -= 1
                return xt, yt
            else:
                return xt, yt

def sol1(input_file: Path) -> List[int]:
    map = dict()
    s = (0,0)
    moves = list()
    with input_file.open('r') as inf:
        for line in inf:
            dir, steps = process_input(line)
            moves.append((dir, steps))
    xh, yh = s
    xt, yt = s
    for dir, steps in moves:
        for step in range(steps):
            if dir == "U":
                xh += 1
            elif dir == "D":
                xh -= 1
            elif dir == "R":
                yh += 1
            elif dir == "L":
                yh -= 1
            xt, yt = next_tail(xh, yh, xt, yt)
            if not (xt,yt) in map:
                map[(xt,yt)] = 0
            map[(xt,yt)] += 1
    print(f"Total: {len(map)}")

def sol2(input_file: Path) -> List[int]:
    map = dict()
    s = (0,0)
    moves = list()
    with input_file.open('r') as inf:
        for line in inf:
            dir, steps = process_input(line)
            moves.append((dir, steps))
    xh, yh = s
    tails = list()
    for i in range(9):
        xt, yt = s
        tails.append((xt,yt))
    for dir, steps in moves:
        for step in range(steps):
            if dir == "U":
                xh += 1
            elif dir == "D":
                xh -= 1
            elif dir == "R":
                yh += 1
            elif dir == "L":
                yh -= 1
            prevx, prevy = xh, yh
            new_tails = list()
            for xt, yt in tails:
                xt, yt = next_tail(prevx, prevy, xt, yt)
                prevx = xt
                prevy = yt
                new_tails.append((xt,yt))
            tails = new_tails
            xt,yt = tails[-1]
            if not (xt,yt) in map:
                map[(xt,yt)] = 0
            map[(xt,yt)] += 1
    print(f"Total: {len(map)}")

def test_1_test():
    input_file = Path('2022/9/test_input.txt')
    results = sol1(input_file)
    print(results)

def test_1():
    input_file = Path('2022/9/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/9/test_input.txt')
    results = sol2(input_file)
    print(results)

def test_2_test2():
    input_file = Path('2022/9/test_input2.txt')
    results = sol2(input_file)
    print(results)

def test_2():
    input_file = Path('2022/9/input.txt')
    result = sol2(input_file)
    print(result)