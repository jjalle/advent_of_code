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

PATTERN = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'

class Item(Enum):
    ORE=0
    CLAY=1
    OBSIDIAN=2
    GEODE=3

class Blueprint:
    def __init__(self, idx: int, orer_ore_cost: int, clar_ore_cost: int, obsr_ore_cost: int, obsr_cla_cost: int, geor_ore_cost: int, geor_obs_cost: int):
        self.idx = idx
        self.orer_ore_cost = orer_ore_cost
        self.clar_ore_cost = clar_ore_cost
        self.obsr_ore_cost = obsr_ore_cost
        self.obsr_cla_cost = obsr_cla_cost
        self.geor_ore_cost = geor_ore_cost
        self.geor_obs_cost = geor_obs_cost
        self.max_orer = max(self.orer_ore_cost, self.clar_ore_cost, self.obsr_ore_cost, self.geor_ore_cost)
        self.max_clayr = self.obsr_cla_cost
        self.max_obsr = self.geor_obs_cost

def dfs(bp: Blueprint, max_geode: int, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int], minutes: int, wait_ore: int, wait_clay: int, wait_obsidian: int):
    if minutes == 0:
        return inventory[3]
    can_ore = can_produce_ore_robot(bp, inventory, robots)
    can_clay = can_produce_clay_robot(bp, inventory, robots)
    can_obsidian = can_produce_obsidian_robot(bp, inventory, robots)
    can_geode = can_produce_geode_robot(bp, inventory, robots)
    new_inv = collect_items(bp, inventory, robots)
    geode = new_inv[3]
    geode_robots = robots[3]
    if can_geode:
        max_possible_geode = geode + (minutes * geode_robots) + (minutes * (minutes - 1)//2)
    else:
        geode_minutes = minutes - 1
        max_possible_geode = geode + (minutes * geode_robots) + (geode_minutes * (geode_minutes - 1)//2)
    if max_possible_geode <= max_geode:
        # Impossible to be better than previous
        return max_geode
    if can_geode:
        # If we can build geode robot, that should be priority
        next_inv, next_robots = produce_geode_robot(bp, new_inv, robots)
        geodes = dfs(bp, max_geode, next_inv, next_robots, minutes - 1, True, True, True)
        if geodes > max_geode:
            return geodes
        else:
            return max_geode
    if can_obsidian and wait_obsidian:
        next_inv, next_robots = produce_obsidian_robot(bp, new_inv, robots)
        geodes = dfs(bp, max_geode, next_inv, next_robots, minutes - 1, True, True, True)
        if geodes > max_geode:
            max_geode = geodes
    if can_clay and wait_clay:
        next_inv, next_robots = produce_clay_robot(bp, new_inv, robots)
        geodes = dfs(bp, max_geode, next_inv, next_robots, minutes - 1, True, True, True)
        if geodes > max_geode:
            max_geode = geodes
    if can_ore and wait_ore:
        next_inv, next_robots = produce_ore_robot(bp, new_inv, robots)
        geodes = dfs(bp, max_geode, next_inv, next_robots, minutes - 1, True, True, True)
        if geodes > max_geode:
            max_geode = geodes
    wait_ore = not can_ore
    wait_clay = not can_clay
    wait_obsidian = not can_obsidian
    geodes = dfs(bp, max_geode, new_inv, robots, minutes - 1, wait_ore, wait_clay, wait_obsidian)
    if geodes > max_geode:
        return geodes
    else:
        return max_geode

def collect_items(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> Tuple[int,int,int,int]:
    ore = inventory[0] + robots[0]
    clay = inventory[1] + robots[1]
    obsidian = inventory[2] + robots[2]
    geode = inventory[3] + robots[3]
    return (ore,clay,obsidian, geode)

def can_produce_ore_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> bool:
    if robots[0] >= bp.max_orer:
        return False
    else:
        return inventory[0] >= bp.orer_ore_cost

def produce_ore_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> Tuple[Tuple[int,int,int,int], Tuple[int,int,int,int]]:
    new_inv = (inventory[0] - bp.orer_ore_cost, inventory[1], inventory[2], inventory[3])
    new_robots = (robots[0] + 1, robots[1], robots[2], robots[3])
    return new_inv, new_robots

def can_produce_clay_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> bool:
    if robots[1] >= bp.max_clayr:
        return False
    else:
        return inventory[0] >= bp.clar_ore_cost

def produce_clay_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> Tuple[Tuple[int,int,int,int], Tuple[int,int,int,int]]:
    new_inv = (inventory[0] - bp.clar_ore_cost, inventory[1], inventory[2], inventory[3])
    new_robots = (robots[0], robots[1] + 1, robots[2], robots[3])
    return new_inv, new_robots

def can_produce_obsidian_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> bool:
    if robots[2] >= bp.max_obsr:
        return False
    else:
        return inventory[0] >= bp.obsr_ore_cost and inventory[1] >= bp.obsr_cla_cost

def produce_obsidian_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> Tuple[Tuple[int,int,int,int], Tuple[int,int,int,int]]:
    new_inv = (inventory[0] - bp.obsr_ore_cost, inventory[1] - bp.obsr_cla_cost, inventory[2], inventory[3])
    new_robots = (robots[0], robots[1], robots[2] + 1, robots[3])
    return new_inv, new_robots

def can_produce_geode_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> bool:
    return inventory[0] >= bp.geor_ore_cost and inventory[2] >= bp.geor_obs_cost

def produce_geode_robot(bp: Blueprint, inventory: Tuple[int,int,int,int], robots: Tuple[int,int,int,int]) -> Tuple[Tuple[int,int,int,int], Tuple[int,int,int,int]]:
    new_inv = (inventory[0] - bp.geor_ore_cost, inventory[1], inventory[2] - bp.geor_obs_cost, inventory[3])
    new_robots = (robots[0], robots[1], robots[2], robots[3] + 1)
    return new_inv, new_robots

def process_line(line: str) -> Blueprint:
    match = re.match(PATTERN, line)
    idx = int(match.group(1))
    orer_ore_cost = int(match.group(2))
    clar_ore_cost = int(match.group(3))
    obsr_ore_cost = int(match.group(4))
    obsr_cla_cost = int(match.group(5))
    geor_ore_cost = int(match.group(6))
    geor_obs_cost = int(match.group(7))
    bp = Blueprint(idx, orer_ore_cost, clar_ore_cost, obsr_ore_cost, obsr_cla_cost, geor_ore_cost, geor_obs_cost)
    return bp

def sol1(input_file: Path) -> List[int]:
    bps: List[Blueprint] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            bp = process_line(line)
            bps.append(bp)
    count = 0
    for bp in bps:
        geodes = dfs(bp, 0, (0, 0, 0, 0), (1, 0, 0, 0), 24, True, True, True)
        value = (bp.idx)*geodes
        print(f"BP({bp.idx}: Max geodes: {geodes}, Value: {value}")
        count += value
    print(f"Result: {count}")

def sol2(input_file: Path) -> List[int]:
    bps: List[Blueprint] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            bp = process_line(line)
            bps.append(bp)
    count = 1
    for bp in bps[0:3]:
        geodes = dfs(bp, 0, (0, 0, 0, 0), (1, 0, 0, 0), 32, True, True, True)
        print(f"BP({bp.idx}: Max geodes: {geodes}")
        count *= geodes
    print(f"Result: {count}")

def test_1_test():
    input_file = Path('2022/19/input_test.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/19/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/19/input_test.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/19/input.txt')
    result = sol2(input_file)
    print(result)