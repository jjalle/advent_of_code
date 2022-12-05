import pytest
from typing import Optional, List, Tuple
from pathlib import Path
from queue import PriorityQueue
import heapq

def process_range(line: str) -> bool:
    ranges = line.split(',')
    rangeA = ranges[0].split('-')
    rangeB = ranges[1].split('-')
    rangeA_min = int(rangeA[0])
    rangeA_max = int(rangeA[1])
    rangeB_min = int(rangeB[0])
    rangeB_max = int(rangeB[1])
    return ( set((range(rangeA_min,rangeA_max+1))).issubset(range(rangeB_min,rangeB_max+1)) or set((range(rangeB_min,rangeB_max+1))).issubset(range(rangeA_min,rangeA_max+1)))
    if rangeA_min >= rangeB_min:
        if rangeA_max <= rangeB_max:
            return True
        else:
            return False
    else:
        if rangeA_max >= rangeB_max:
            return True
        else:
            return False

def process_range2(line: str) -> bool:
    ranges = line.split(',')
    rangeA = ranges[0].split('-')
    rangeB = ranges[1].split('-')
    rangeA_min = int(rangeA[0])
    rangeA_max = int(rangeA[1])
    rangeB_min = int(rangeB[0])
    rangeB_max = int(rangeB[1])
    rA = set(range(rangeA_min,rangeA_max+1))
    rB = set(range(rangeB_min,rangeB_max+1))
    return len(rA.intersection(rB)) > 0

def sol1(input_file: Path) -> int:
    result = 0
    with input_file.open('r') as inf:
        for line in inf:
            included = process_range(line)
            if included:
                result += 1
    return result

def sol2(input_file: Path) -> int:
    result = 0
    with input_file.open('r') as inf:
        for line in inf:
            included = process_range2(line)
            if included:
                result += 1
    return result

def test_1_test():
    input_file = Path('2022/4/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/4/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/4/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/4/input.txt')
    result = sol2(input_file)
    print(result)