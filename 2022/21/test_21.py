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

SUM_PATTERN = r'([a-z]{4}): ([a-z]{4}) \+ ([a-z]{4})'
SUB_PATTERN = r'([a-z]{4}): ([a-z]{4}) - ([a-z]{4})'
MULT_PATTERN = r'([a-z]{4}): ([a-z]{4}) \* ([a-z]{4})'
DIV_PATTERN = r'([a-z]{4}): ([a-z]{4}) \/ ([a-z]{4})'
LITERAL_PATTERN = r'([a-z]{4}): (\d+)'

class Type(Enum):
    NONE=0
    SUM=1
    SUB=2
    MULT=3
    DIV=4

class Node:
    def __init__(self, label: str):
        self.label = label
    def resolve(self) -> float:
        pass
    def reverse(self, result: float) -> float:
        pass
    def has_human(self) -> bool:
        pass
    def connect(self, nodes: Dict[str, 'Node']):
        pass
    def root_resolve(self) -> float:
        pass

class Operation(Node):
    def __init__(self, label: str, type: Type, op1_label: str, op2_label: str):
        super().__init__(label)
        self.type = type
        self.op1_label = op1_label
        self.op2_label = op2_label
        self.op1: Node = None
        self.op2: Node = None
    def connect(self, nodes: Dict[str, Node]):
        self.op1 = nodes[self.op1_label]
        self.op2 = nodes[self.op2_label]
    def root_resolve(self) -> float:
        if self.op1.has_human():
            if self.op2.has_human():
                raise RuntimeError(f"Impossible")
            result = self.op2.resolve()
            return self.op1.reverse(result)
        elif self.op2.has_human():
            if self.op1.has_human():
                raise RuntimeError(f"Impossible")
            result = self.op1.resolve()
            return self.op2.reverse(result)
        else:
            raise RuntimeError(f"Impossible")
    def reverse(self, result: float) -> float:
        if self.op1.has_human():
            tmp = self.op2.resolve()
            if self.type == Type.SUM:
                op1 = result - tmp
                return self.op1.reverse(op1)
            elif self.type == Type.SUB:
                op1 = result + tmp
                return self.op1.reverse(op1)
            elif self.type == Type.MULT:
                op1 = result / tmp
                return self.op1.reverse(op1)
            elif self.type == Type.DIV:
                op1 = result * tmp
                return self.op1.reverse(op1)
            else:
                raise RuntimeError(f"Impossible")
        elif self.op2.has_human():
            tmp = self.op1.resolve()
            if self.type == Type.SUM:
                op2 = result - tmp
                return self.op2.reverse(op2)
            elif self.type == Type.SUB:
                op2 = tmp - result
                return self.op2.reverse(op2)
            elif self.type == Type.MULT:
                op2 = result / tmp
                return self.op2.reverse(op2)
            elif self.type == Type.DIV:
                op2 = tmp / result
                return self.op2.reverse(op2)
            else:
                raise RuntimeError(f"Impossible")
        else:
            raise RuntimeError(f"Impossible")
    def resolve(self) -> float:
        op1 = self.op1.resolve()
        op2 = self.op2.resolve()
        if self.type == Type.SUM:
            return op1 + op2
        elif self.type == Type.SUB:
            return op1 - op2
        elif self.type == Type.MULT:
            return op1 * op2
        elif self.type == Type.DIV:
            return op1 / op2
        else:
            raise RuntimeError(f"Impossible")
    def has_human(self) -> bool:
        return self.op1.has_human() or self.op2.has_human()

class Literal(Node):
    def __init__(self, label: str, value: float):
        super().__init__(label)
        self.value = value
    def resolve(self) -> float:
        return self.value
    def reverse(self, result: float) -> float:
        if self.has_human():
            return result
        else:
            raise RuntimeError(f"Impossible")
    def has_human(self) -> bool:
        return self.label == "humn"

def process_line(line: str) -> Node:
    sum_match = re.match(SUM_PATTERN, line)
    sub_match = re.match(SUB_PATTERN, line)
    mul_match = re.match(MULT_PATTERN, line)
    div_match = re.match(DIV_PATTERN, line)
    lit_match = re.match(LITERAL_PATTERN, line)
    if sum_match:
        label = sum_match.group(1)
        op1 = sum_match.group(2)
        op2 = sum_match.group(3)
        return Operation(label, Type.SUM, op1, op2)
    elif sub_match:
        label = sub_match.group(1)
        op1 = sub_match.group(2)
        op2 = sub_match.group(3)
        return Operation(label, Type.SUB, op1, op2)
    elif mul_match:
        label = mul_match.group(1)
        op1 = mul_match.group(2)
        op2 = mul_match.group(3)
        return Operation(label, Type.MULT, op1, op2)
    elif div_match:
        label = div_match.group(1)
        op1 = div_match.group(2)
        op2 = div_match.group(3)
        return Operation(label, Type.DIV, op1, op2)
    elif lit_match:
        label = lit_match.group(1)
        value = float(lit_match.group(2))
        return Literal(label, value)
    else:
        raise RuntimeError(f"Impossible")

def sol1(input_file: Path) -> List[int]:
    print(f"")
    nodes: Dict[str, Node] = dict()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            node = process_line(line)
            nodes[node.label] = node
    for node in nodes.values():
        node.connect(nodes)
    root = nodes["root"]
    result = root.resolve()
    print(f"Result: {result}")

def sol2(input_file: Path) -> List[int]:
    print(f"")
    nodes: Dict[str, Node] = dict()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            node = process_line(line)
            nodes[node.label] = node
    for node in nodes.values():
        node.connect(nodes)
    root = nodes["root"]
    result = root.root_resolve()
    print(f"Result: {result}")

def test_1_test():
    input_file = Path('2022/21/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/21/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/21/input_test.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/21/input.txt')
    result = sol2(input_file)
    print(result)