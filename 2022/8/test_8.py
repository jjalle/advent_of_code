import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict
import re

def process_input(line: str) -> List[int]:
    line = line.strip()
    result = list()
    for char in line:
        result.append(int(char))
    return result

def get_scenic_score(r: int, c: int, nr: int, nc: int, trees: List[List[int]]) -> bool:
    tree = trees[r][c]
    up_score = 0
    down_score = 0
    left_score = 0
    right_score = 0
    # Check up
    for i in range(r-1, -1, -1):
        up_score += 1
        other_tree = trees[i][c]
        if other_tree >= tree:
            break
    if up_score == 0:
        return 0
    # Check down
    for i in range(r+1, nr):
        down_score += 1
        other_tree = trees[i][c]
        if other_tree >= tree:
            break
    if down_score == 0:
        return 0
    # Check left
    for j in range(c-1, -1, -1):
        left_score += 1
        other_tree = trees[r][j]
        if other_tree >= tree:
            break
    if left_score == 0:
        return 0
    # Check right
    for j in range(c+1, nc):
        right_score += 1
        other_tree = trees[r][j]
        if other_tree >= tree:
            break
    if right_score == 0:
        return 0
    score = up_score * down_score * left_score * right_score
    return score

def is_tree_visible(r: int, c: int, nr: int, nc: int, trees: List[List[int]]) -> bool:
    if r == 0 or r == nr - 1:
        return True
    if c == 0 or c == nc - 1:
        return True
    tree = trees[r][c]
    # Check up
    visible = True
    for i in range(r):
        other_tree = trees[i][c]
        if other_tree >= tree:
            visible = False
    if visible:
        return True
    # Check down
    visible = True
    for i in range(r+1, nr):
        other_tree = trees[i][c]
        if other_tree >= tree:
            visible = False
    if visible:
        return True
    # Check left
    visible = True
    for j in range(c):
        other_tree = trees[r][j]
        if other_tree >= tree:
            visible = False
    if visible:
        return True
    # Check right
    visible = True
    for j in range(c+1, nc):
        other_tree = trees[r][j]
        if other_tree >= tree:
            visible = False
    if visible:
        return True
    return False

def sol1(input_file: Path) -> List[int]:
    trees = list()
    with input_file.open('r') as inf:
        for line in inf:
            row = process_input(line)
            trees.append(row)
    nr = len(trees)
    nc = len(trees[0])
    visible_trees = 0
    for r in range(nr):
        for c in range(nc):
            visible = is_tree_visible(r, c, nr, nc, trees)
            if visible:
                visible_trees += 1
    print(f"Total: {visible_trees}")

def sol2(input_file: Path) -> List[int]:
    trees = list()
    with input_file.open('r') as inf:
        for line in inf:
            row = process_input(line)
            trees.append(row)
    nr = len(trees)
    nc = len(trees[0])
    scenic_score = 0
    for r in range(nr):
        for c in range(nc):
            score = get_scenic_score(r, c, nr, nc, trees)
            if score > scenic_score:
                scenic_score = score
    print(f"Total: {scenic_score}")

def test_1_test():
    input_file = Path('2022/8/test_input.txt')
    results = sol1(input_file)
    print(results)

def test_1():
    input_file = Path('2022/8/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/8/test_input.txt')
    results = sol2(input_file)
    print(results)

def test_2():
    input_file = Path('2022/8/input.txt')
    result = sol2(input_file)
    print(result)