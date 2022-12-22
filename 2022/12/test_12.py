import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict, deque
import re

def process_line(line: str) -> Tuple[List[int], int, int]:
    line = line.strip()
    result = list()
    start = None
    end = None
    for idx, char in enumerate(line):
        if char == "S":
            value = 0
            start = idx
        elif char == "E":
            value = ord('z') - ord('a') + 2
            end = idx
        else:
            value = ord(char) - ord('a') + 1
        result.append(value)
    return result, start, end

def process_line2(line: str) -> Tuple[List[int], List[int], int]:
    line = line.strip()
    result = list()
    start = list()
    end = None
    for idx, char in enumerate(line):
        if char == "S":
            value = 1
            start.append(idx)
        elif char == "E":
            value = ord('z') - ord('a') + 2
            end = idx
        else:
            value = ord(char) - ord('a') + 1
            if value == 1:
                start.append(idx)
        result.append(value)
    return result, start, end

def sol1(input_file: Path) -> List[int]:
    map = list()
    start = None
    end = None
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            row, start_col, end_col = process_line(line)
            if start_col is not None:
                start = (idx, start_col)
            if end_col is not None:
                end = (idx, end_col)
            map.append(row)
    nr = len(map)
    nc = len(map[0])
    print("")
    print(f"Map: {nr} by {nc}, Start: {start}, End: {end}")
    visited = list()
    for r in range(nr):
        row = list()
        for c in range(nc):
            row.append(False)
        visited.append(row)
    q = deque()
    q.append((*start, 0))
    while len(q):
        x, y, steps = q.popleft()
        if (x,y) == end:
            print(f"Reached end at {steps} steps")
            break
        if not visited[x][y]:
            visited[x][y] = True
            val = map[x][y]
            for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
                if nx >= 0 and nx < nr and ny >= 0 and ny < nc:
                    if not visited[nx][ny]:
                        nval = map[nx][ny]
                        if nval > val + 1:
                            # Skip
                            pass
                        else:
                            q.append((nx, ny, steps + 1))

def sol2(input_file: Path) -> List[int]:
    map = list()
    starts = list()
    end = None
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            row, source_cols, end_col = process_line2(line)
            for source_col in source_cols:
                starts.append((idx, source_col))
            if end_col is not None:
                end = (idx, end_col)
            map.append(row)
    nr = len(map)
    nc = len(map[0])
    print("")
    print(f"Map: {nr} by {nc}, Starts: {starts}, End: {end}")
    visited = list()
    for r in range(nr):
        row = list()
        for c in range(nc):
            row.append(False)
        visited.append(row)
    q = deque()
    for start in starts:
        q.append((*start, 0))
    while len(q):
        x, y, steps = q.popleft()
        if (x,y) == end:
            print(f"Reached end at {steps} steps")
            break
        if not visited[x][y]:
            visited[x][y] = True
            val = map[x][y]
            for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
                if nx >= 0 and nx < nr and ny >= 0 and ny < nc:
                    if not visited[nx][ny]:
                        nval = map[nx][ny]
                        if nval > val + 1:
                            # Skip
                            pass
                        else:
                            q.append((nx, ny, steps + 1))

def test_1_test():
    input_file = Path('2022/12/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/12/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/12/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/12/input.txt')
    result = sol2(input_file)
    print(result)