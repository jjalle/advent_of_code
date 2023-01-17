import pytest
from typing import Optional, List, Tuple, Set, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict, deque
import re
import json
import copy
from enum import Enum, IntEnum
from functools import cmp_to_key
import itertools
import math

def process_line(line: str) -> int:
    number = 0
    for idx, c in enumerate(line):
        number *= 5
        if c == '2':
            number += 2
        elif c == '1':
            number += 1
        elif c == '0':
            number += 0
        elif c == '-':
            number -= 1
        elif c == '=':
            number -= 2
        else:
            raise RuntimeError(f"Impossible")
    return number

def to_snafu(number: int) -> str:
    result = ""
    remainder = number
    while True:
        this_pow_of_5 = 0
        char = ""
        rest = remainder % 5
        if rest == 4:
            this_pow_of_5 = -1
            char = "-"
        elif rest == 3:
            this_pow_of_5 = -2
            char = "="
        elif rest == 2:
            this_pow_of_5 = 2
            char = "2"
        elif rest == 1:
            this_pow_of_5 = 1
            char = "1"
        elif rest == 0:
            this_pow_of_5 = 0
            char = "0"
        else:
            raise RuntimeError(f"Impossible")
        result += char
        remainder -= this_pow_of_5
        if remainder == 0:
            break
        else:
            remainder /= 5
    return result[::-1]

def sol1(input_file: Path) -> List[int]:
    print(f"")
    numbers = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            num = process_line(line)
            numbers.append(num)
    print(numbers)
    total = sum(numbers)
    result = to_snafu(total)
    print(f"Result: {result}")

def sol2(input_file: Path) -> List[int]:
    pass

def test_1_small():
    input_file = Path('2022/25/input_test_small.txt')
    result = sol1(input_file)
    for i in [1,2,3,4,5,6,7,8,9,10,15,20,2022,12345,314159265]:
        num = to_snafu(i)
        print(f"{i} = {num}")
    print(result)

def test_1_test():
    input_file = Path('2022/25/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/25/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/25/input_test.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/25/input.txt')
    result = sol2(input_file)
    print(result)