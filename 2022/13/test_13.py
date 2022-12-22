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

class Result(Enum):
    RIGHT_ORDER=0
    EQUAL=1
    BAD_ORDER=2

def process_line(line: str) -> list:
    data = json.loads(line)
    return data

def check_result(a: list, b: list) -> Result:
    if isinstance(a, list) and isinstance(b, list):
        for ca, cb in zip(a, b):
            cres= check_result(ca, cb)
            if cres == Result.RIGHT_ORDER:
                return Result.RIGHT_ORDER
            elif cres == Result.BAD_ORDER:
                return Result.BAD_ORDER
            else:
                continue
        if len(b) < len(a):
            return Result.BAD_ORDER
        elif len(a) < len(b):
            return Result.RIGHT_ORDER
        else:
            return Result.EQUAL
    elif isinstance(a, int) and isinstance(b, list):
        la = [a]
        return check_result(la, b)
    elif isinstance(a, list) and isinstance(b, int):
        lb = [b]
        return check_result(a, lb)
    elif isinstance(a, int) and isinstance(b, int):
        if a > b:
            return Result.BAD_ORDER
        elif a < b:
            return Result.RIGHT_ORDER
        else:
            return Result.EQUAL
    else:
        raise RuntimeError(f"Impossible")

def sol1(input_file: Path) -> List[int]:
    lines = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            if line:
                data = process_line(line)
                lines.append(data)
    la = lines[0::2]
    lb = lines[1::2]
    count = 0
    for idx, (a,b) in enumerate(zip(la,lb)):
        result = check_result(a,b)
        if result == Result.RIGHT_ORDER:
            count += idx + 1
    print(f"Result: {count}")

def compare(item1, item2):
    result = check_result(item1, item2)
    if result == Result.RIGHT_ORDER:
        return -1
    elif result == Result.BAD_ORDER:
        return 1
    else:
        return 0

def sol2(input_file: Path) -> List[int]:
    lines = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            if line:
                data = process_line(line)
                lines.append(data)
    lines.append([[2]])
    lines.append([[6]])
    ordered_items = sorted(lines, key=cmp_to_key(compare))
    divisor1 = None
    divisor2 = None
    for idx, item in enumerate(ordered_items):
        if item == [[2]]:
            divisor1 = idx + 1
        elif item == [[6]]:
            divisor2 = idx + 1
    if divisor1 is None or divisor2 is None:
        print("Error")
    else:
        result = divisor1 * divisor2
        print(f"Result: {result}")

def test_1_test():
    input_file = Path('2022/13/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/13/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/13/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/13/input.txt')
    result = sol2(input_file)
    print(result)