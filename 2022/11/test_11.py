import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict
import re

test_max_product = 23 * 19 * 13 *17

class TestMonkey0:
    def __init__(self):
        self.items: List[int] = [79, 98]
    def operate(self, old: int):
        return old*19
    def test(self, value: int) -> int:
        if value % 23 == 0:
            return 2
        else:
            return 3

class TestMonkey1:
    def __init__(self):
        self.items: List[int] = [54, 65, 75, 74]
    def operate(self, old: int):
        return old + 6
    def test(self, value: int) -> int:
        if value % 19 == 0:
            return 2
        else:
            return 0

class TestMonkey2:
    def __init__(self):
        self.items: List[int] = [79, 60, 97]
    def operate(self, old: int):
        return old * old
    def test(self, value: int) -> int:
        if value % 13 == 0:
            return 1
        else:
            return 3

class TestMonkey3:
    def __init__(self):
        self.items: List[int] = [74]
    def operate(self, old: int):
        return old + 3
    def test(self, value: int) -> int:
        if value % 17 == 0:
            return 0
        else:
            return 1

max_product = 11 * 19 * 5 * 2 * 13 * 7 * 3 * 17

class Monkey0:
    def __init__(self):
        self.items: List[int] = [97, 81, 57, 57, 91, 61]
    def operate(self, old: int):
        return old * 7
    def test(self, value: int) -> int:
        if value % 11 == 0:
            return 5
        else:
            return 6

class Monkey1:
    def __init__(self):
        self.items: List[int] = [88, 62, 68, 90]
    def operate(self, old: int):
        return old * 17
    def test(self, value: int) -> int:
        if value % 19 == 0:
            return 4
        else:
            return 2

class Monkey2:
    def __init__(self):
        self.items: List[int] = [74, 87]
    def operate(self, old: int):
        return old + 2
    def test(self, value: int) -> int:
        if value % 5 == 0:
            return 7
        else:
            return 4

class Monkey3:
    def __init__(self):
        self.items: List[int] = [53, 81, 60, 87, 90, 99, 75]
    def operate(self, old: int):
        return old + 1
    def test(self, value: int) -> int:
        if value % 2 == 0:
            return 2
        else:
            return 1

class Monkey4:
    def __init__(self):
        self.items: List[int] = [57]
    def operate(self, old: int):
        return old + 6
    def test(self, value: int) -> int:
        if value % 13 == 0:
            return 7
        else:
            return 0

class Monkey5:
    def __init__(self):
        self.items: List[int] = [54, 84, 91, 55, 59, 72, 75, 70]
    def operate(self, old: int):
        return old * old
    def test(self, value: int) -> int:
        if value % 7 == 0:
            return 6
        else:
            return 3

class Monkey6:
    def __init__(self):
        self.items: List[int] = [95, 79, 79, 68, 78]
    def operate(self, old: int):
        return old + 3
    def test(self, value: int) -> int:
        if value % 3 == 0:
            return 1
        else:
            return 3

class Monkey7:
    def __init__(self):
        self.items: List[int] = [61, 97, 67]
    def operate(self, old: int):
        return old + 4
    def test(self, value: int) -> int:
        if value % 17 == 0:
            return 0
        else:
            return 5

test_setup = [
    TestMonkey0(),
    TestMonkey1(),
    TestMonkey2(),
    TestMonkey3(),
]

setup = [
    Monkey0(),
    Monkey1(),
    Monkey2(),
    Monkey3(),
    Monkey4(),
    Monkey5(),
    Monkey6(),
    Monkey7()
]

def sol1(setup, rounds: int) -> List[int]:
    print(f"")
    inspects = list()
    for monkey in setup:
        inspects.append(0)
    for round in range(rounds):
        for idx, monkey in enumerate(setup):
            for item in monkey.items:
                val = monkey.operate(item)
                val = val // 3
                next_monkey = monkey.test(val)
                setup[next_monkey].items.append(val)
                inspects[idx] += 1
            monkey.items = list()
        print(f"")
        print(f"After round {round +1}, the monkeys are holding items with these worry levels:")
        for idx, monkey in enumerate(setup):
            items = [str(val) for val in monkey.items]
            msg = ', '.join(items)
            print(f"Monkey {idx}: {msg}")
    largest = heapq.nlargest(2, inspects)
    print(largest)
    result = largest[0] * largest[1]
    print(f"Result: {result}")

def sol2(setup, max_val: int, rounds: int) -> List[int]:
    print(f"")
    print_points = [
        1, 20, 1000, 2000, 3000, 4000, 5000, 
        6000, 7000, 8000, 9000, 10000
    ]
    inspects = list()
    for monkey in setup:
        inspects.append(0)
    for round in range(rounds):
        for idx, monkey in enumerate(setup):
            for item in monkey.items:
                val = monkey.operate(item)
                val = val % max_val
                next_monkey = monkey.test(val)
                setup[next_monkey].items.append(val)
                inspects[idx] += 1
            monkey.items = list()
        for point in print_points:
            if round + 1 == point:
                print(f"")
                print(f"== After round {point} ==")
                for idx, monkey in enumerate(setup):
                    print(f"Monkey {idx} inspected items {inspects[idx]} times.")
                break
    largest = heapq.nlargest(2, inspects)
    print(largest)
    result = largest[0] * largest[1]
    print(f"Result: {result}")

def test_1_test():
    input_file = Path('2022/11/test_input.txt')
    results = sol1(test_setup, 20)
    print(results)

def test_1():
    input_file = Path('2022/11/input.txt')
    result = sol1(setup, 20)
    print(result)

def test_2_test():
    input_file = Path('2022/11/test_input.txt')
    results = sol2(test_setup, test_max_product, 10000)
    print(results)

def test_2():
    input_file = Path('2022/11/input.txt')
    result = sol2(setup, max_product, 10000)
    print(result)