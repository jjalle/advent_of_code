import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict
import re

PATTERN = r'move ([0-9]+) from ([0-9]+) to ([0-9]+)'

def parse_crates(line: str, crates: Dict[int, List[str]]) -> Dict[int, List[str]]:
    chars = len(line) - 1
    for i in range(0, chars, 4):
        idx = i // 4
        crate = line[i+1]
        if crate != " ":
            if not idx in crates:
                crates[idx] = list()
            crates[idx].append(crate)
    return crates

def parse_move(line: str) -> Tuple[int, int, int]:
    result = re.match(PATTERN, line)
    n = int(result.group(1))
    src = int(result.group(2))
    dst = int(result.group(3))
    return n, src, dst

def sol1(input_file: Path) -> int:
    stage = 0
    crates: Dict[int, List[str]] = OrderedDict()
    moves: List[Tuple[int, int, int]] = list()
    with input_file.open('r') as inf:
        for line in inf:
            if stage == 0:
                if "[" in line:
                    crates = parse_crates(line, crates)
                else:
                    stage = 1
            elif line != "\n":
                n, src, dst = parse_move(line)
                moves.append((n,src,dst))
    for key, values in crates.items():
        values.reverse()
    for n, src, dst in moves:
        for i in range(n):
            crate = crates[src - 1].pop()
            crates[dst - 1].append(crate)
    result = ""
    n = len(crates)
    for i in range(n):
        values = crates[i]
        top = values[-1]
        result += top
    return result

def sol2(input_file: Path) -> int:
    stage = 0
    crates: Dict[int, List[str]] = OrderedDict()
    moves: List[Tuple[int, int, int]] = list()
    with input_file.open('r') as inf:
        for line in inf:
            if stage == 0:
                if "[" in line:
                    crates = parse_crates(line, crates)
                else:
                    stage = 1
            elif line != "\n":
                n, src, dst = parse_move(line)
                moves.append((n,src,dst))
    for key, values in crates.items():
        values.reverse()
    for n, src, dst in moves:
        to_move = list()
        for i in range(n):
            to_move.append(crates[src - 1].pop())
        to_move.reverse()
        crates[dst - 1].extend(to_move)
    result = ""
    n = len(crates)
    for i in range(n):
        values = crates[i]
        top = values[-1]
        result += top
    return result

def test_1_test():
    input_file = Path('2022/5/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/5/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/5/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/5/input.txt')
    result = sol2(input_file)
    print(result)