import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict
import re

def process_line(line: str) -> int:
    line.strip()
    for i in range(len(line) - 4):
        chars = set()
        chars.add(line[i])
        chars.add(line[i+1])
        chars.add(line[i+2])
        chars.add(line[i+3])
        if len(chars) == 4:
            return i + 4
    return None

def process_line2(line: str) -> int:
    line.strip()
    for i in range(len(line) - 4):
        chars = set()
        for j in range(14):
            chars.add(line[i + j])
        if len(chars) == 14:
            return i + 14
    return None

def sol1(input_file: Path) -> List[int]:
    results = list()
    with input_file.open('r') as inf:
        for line in inf:
            result = process_line(line)
            results.append(result)
    return results

def sol2(input_file: Path) -> List[int]:
    results = list()
    with input_file.open('r') as inf:
        for line in inf:
            result = process_line2(line)
            results.append(result)
    return results


def test_1_test():
    input_file = Path('2022/6/test_input.txt')
    results = sol1(input_file)
    print(results)

def test_1():
    input_file = Path('2022/6/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/6/test_input.txt')
    results = sol2(input_file)
    print(results)

def test_2():
    input_file = Path('2022/6/input.txt')
    result = sol2(input_file)
    print(result)