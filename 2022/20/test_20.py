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

def process_line(line: str) -> int:
    return int(line)

def shift_right(nums: List[int], new_indexes_by_orig_index: Dict[int, int], orig_indexes_by_new_index: Dict[int, int], idx: int, value: int) -> List[int]:
    n = len(nums)
    count = 0
    orig_idx = idx
    curr_idx = new_indexes_by_orig_index[orig_idx]
    while count < value:
        # Shift once
        next_idx = (curr_idx + 1) % n
        # Have we wrapped?
        if next_idx == n-1:
            orig = nums[n-2]
            orig_idx = orig_indexes_by_new_index[n-2]
            # Shift everything right until i == 1
            for i in range(n-2,0,-1):
                nums[i] = nums[i-1]
                i_orig_index = orig_indexes_by_new_index[i-1]
                new_indexes_by_orig_index[i_orig_index] = i
                orig_indexes_by_new_index[i] = i_orig_index
            nums[0] = orig
            new_indexes_by_orig_index[orig_idx] = 0
            orig_indexes_by_new_index[0] = orig_idx
            curr_idx = 0
            count += 1
        else:
            tmp = nums[next_idx]
            nums[next_idx] = nums[curr_idx]
            nums[curr_idx] = tmp
            tmp_next = orig_indexes_by_new_index[next_idx]
            tmp_curr = orig_indexes_by_new_index[curr_idx]
            orig_indexes_by_new_index[next_idx] = tmp_curr
            orig_indexes_by_new_index[curr_idx] = tmp_next
            new_indexes_by_orig_index[tmp_next] = curr_idx
            new_indexes_by_orig_index[tmp_curr] = next_idx
            curr_idx = next_idx
            count += 1
    return

def shift_left(nums: List[int], new_indexes_by_orig_index: Dict[int, int], orig_indexes_by_new_index: Dict[int, int], idx: int, value: int) -> List[int]:
    n = len(nums)
    count = 0
    orig_idx = idx
    curr_idx = new_indexes_by_orig_index[orig_idx]
    while count < value:
        # Shift once
        next_idx = (curr_idx - 1) % n
        # Have we wrapped?
        if next_idx == 0:
            orig = nums[1]
            orig_idx = orig_indexes_by_new_index[1]
            # Shift everything left until i == n-1
            for i in range(1,n-1):
                nums[i] = nums[i+1]
                i_orig_index = orig_indexes_by_new_index[i+1]
                new_indexes_by_orig_index[i_orig_index] = i
                orig_indexes_by_new_index[i] = i_orig_index
            nums[n-1] = orig
            new_indexes_by_orig_index[orig_idx] = n-1
            orig_indexes_by_new_index[n-1] = orig_idx
            curr_idx = n-1
            count += 1
        else:
            tmp = nums[next_idx]
            nums[next_idx] = nums[curr_idx]
            nums[curr_idx] = tmp
            tmp_next = orig_indexes_by_new_index[next_idx]
            tmp_curr = orig_indexes_by_new_index[curr_idx]
            orig_indexes_by_new_index[next_idx] = tmp_curr
            orig_indexes_by_new_index[curr_idx] = tmp_next
            new_indexes_by_orig_index[tmp_next] = curr_idx
            new_indexes_by_orig_index[tmp_curr] = next_idx
            curr_idx = next_idx
            count += 1
    return

def shift(nums: List[int], new_indexes_by_orig_index: Dict[int, int], orig_indexes_by_new_index: Dict[int, int], idx: int, value: int) -> List[int]:
    n = len(nums)
    count = abs(value) % (n - 1)
    if value >= 0:
        shift_right(nums, new_indexes_by_orig_index, orig_indexes_by_new_index, idx, count)
    else:
        shift_left(nums, new_indexes_by_orig_index, orig_indexes_by_new_index, idx, count)

def get_pos_after_zero(nums: List[int], pos: int) -> int:
    zero_idx = None
    for idx, num in enumerate(nums):
        if num == 0:
            if zero_idx is not None:
                raise RuntimeError(f"Impossible")
            zero_idx = idx
    if zero_idx is None:
        raise RuntimeError(f"Impossible")
    n = len(nums)
    result_idx = (zero_idx + pos) % n
    return nums[result_idx]

def sol1(input_file: Path) -> List[int]:
    print(f"")
    nums: List[int] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            num = process_line(line)
            nums.append(num)
    curr = nums.copy()
    n = len(nums)
    new_indexes_by_orig_index = { idx:idx for idx, num in enumerate(nums) }
    orig_indexes_by_new_index = { idx:idx for idx, num in enumerate(nums) }
    for idx, num in enumerate(nums):
        shift(curr, new_indexes_by_orig_index, orig_indexes_by_new_index, idx, num)
        if len(nums) < 10:
            curr_idx = new_indexes_by_orig_index[idx]
            prev = (curr_idx - 1) % n
            nxt = (curr_idx + 1) % n
            print(f"{num} moves between {curr[prev]} and {curr[nxt]}:")
            str_nums = [str(val) for val in curr]
            print(f"[{', '.join(str_nums)}]")
    pos_1000 = get_pos_after_zero(curr, 1000)
    pos_2000 = get_pos_after_zero(curr, 2000)
    pos_3000 = get_pos_after_zero(curr, 3000)
    print(f"the 1000th number after 0 is {pos_1000}")
    print(f"the 2000th number after 0 is {pos_2000}")
    print(f"the 3000th number after 0 is {pos_3000}")
    count = pos_1000 + pos_2000 + pos_3000
    print(f"Result: {count}")

def sol2(input_file: Path) -> List[int]:
    print(f"")
    nums: List[int] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            num = process_line(line)
            nums.append(num*811589153)
    curr = nums.copy()
    n = len(nums)
    new_indexes_by_orig_index = { idx:idx for idx, num in enumerate(nums) }
    orig_indexes_by_new_index = { idx:idx for idx, num in enumerate(nums) }
    for round in range(0,10):
        for idx, num in enumerate(nums):
            shift(curr, new_indexes_by_orig_index, orig_indexes_by_new_index, idx, num)
        if len(nums) < 10:
            print(f"After {round+1} round{'s' if round > 0 else ''} of mixing:")
            str_nums = [str(val) for val in curr]
            print(f"[{', '.join(str_nums)}]")
    pos_1000 = get_pos_after_zero(curr, 1000)
    pos_2000 = get_pos_after_zero(curr, 2000)
    pos_3000 = get_pos_after_zero(curr, 3000)
    print(f"the 1000th number after 0 is {pos_1000}")
    print(f"the 2000th number after 0 is {pos_2000}")
    print(f"the 3000th number after 0 is {pos_3000}")
    count = pos_1000 + pos_2000 + pos_3000
    print(f"Result: {count}")

def test_1_test():
    input_file = Path('2022/20/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/20/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/20/input_test.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/20/input.txt')
    result = sol2(input_file)
    print(result)