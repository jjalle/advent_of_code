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
    cmd = tokens[0]
    if len(tokens) > 1:
        value = int(tokens[1])
    else:
        value = None
    return cmd, value

def get_result(cycle: int, x: int) -> int:
    special_points = [20, 60, 100, 140, 180, 220]
    for point in special_points:
        if cycle == point:
            strength = x*cycle
            print(f"During the {cycle}th cycle, register X has the value {x}, so the signal strength is {cycle} * {x} = {strength}.")
            return strength
    #print(f"During the {cycle}th cycle, register X has the value {x}")
    return None

class Computer:
    def __init__(self):
        self.cycle = 1
        self.x = 1
        self.pending = list()
        self.current = ("noop", None, 0)
        self.total_strength = 0
        self.output = list()
    def add_cmd(self, new_cmd: str, new_value: int):
        if new_cmd == "addx":
            delay = 1
        else:
            delay = 0
        self.pending.append((new_cmd, new_value, delay))
    def step(self):
        cmd, value, delay = self.current
        if delay != 0:
            delay -= 1
            self.current = (cmd, value, delay)
        else:
            # Execute pipeline
            if cmd == "addx":
                self.x += value
            if self.pending:
                self.current = self.pending[0]
                self.pending = self.pending[1:]
            else:
                self.current = ("noop", None, 0)
        # Check for signal strength
        strength = get_result(self.cycle, self.x)
        if strength:
            self.total_strength += strength
        print(f"{self.cycle}, {cmd}, {value}, {delay}, {self.x}")
        # Check for output
        row = ((self.cycle - 1) // 40) % 6
        col = (self.cycle - 1) % 40
        if len(self.output) <= row:
            self.output.append(list())
        line = self.output[row]
        if self.x == col or self.x - 1 == col or self.x + 1 == col:
            line.append("#")
        else:
            line.append(".")
        self.cycle += 1
    def has_work(self):
        return len(self.pending) > 0 or self.current[0] == "addx"
    def print_output(self):
        x = list()
        for line in self.output:
            row = ''.join(line)
            x.append(row)
        result = '\n'.join(x)
        print(result)

def sol1(input_file: Path) -> List[int]:
    print(f"")
    cpu = Computer()
    with input_file.open('r') as inf:
        for line in inf:
            cmd, value = process_input(line)
            cpu.add_cmd(cmd, value)
            cpu.step()
    while cpu.has_work():
        cpu.step()
    print(f"Total: {cpu.total_strength}")

def sol2(input_file: Path) -> List[int]:
    print(f"")
    cpu = Computer()
    with input_file.open('r') as inf:
        for line in inf:
            cmd, value = process_input(line)
            cpu.add_cmd(cmd, value)
            cpu.step()
    while cpu.has_work():
        cpu.step()
    print(f"Total: {cpu.total_strength}")
    cpu.print_output()

def test_1_test():
    input_file = Path('2022/10/test_input1.txt')
    results = sol1(input_file)
    print(results)

def test_1_test2():
    input_file = Path('2022/10/test_input2.txt')
    results = sol1(input_file)
    print(results)

def test_1():
    input_file = Path('2022/10/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/10/test_input2.txt')
    results = sol2(input_file)
    print(results)

def test_2():
    input_file = Path('2022/10/input.txt')
    result = sol2(input_file)
    print(result)