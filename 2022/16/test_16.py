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

PATTERN = r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)'

class Node:
    def __init__(self, label: str, id: int, rate: int):
        self.label = label
        self.id = id
        self.rate = rate
        self.neighbors: List['Node'] = list()
    def add_neighbor(self, node: 'Node'):
        self.neighbors.append(node)

def process_line(idx: int, line: str) -> Tuple[Node, List[str]]:
    match = re.match(PATTERN, line)
    if not match:
        raise RuntimeError(f"Impossible")
    valve = match.group(1)
    flow = int(match.group(2))
    node = Node(valve, idx, flow)
    neighbors = list()
    for token in match.group(3).split(', '):
        neighbors.append(token.strip())
    return node, neighbors

def get_graph(entries: List[Tuple[Node, List[str]]]) -> Node:
    nodes = dict()
    for node, _ in entries:
        nodes[node.label] = node
    for node, neighbors in entries:
        for neighbor in neighbors:
            nnode = nodes[neighbor]
            node.add_neighbor(nnode)
    return nodes['AA']

def floyd_warshall(graph: Node, n: int) -> Tuple[List[List[int]], List[int]]:
    dist = list()
    for i in range(n):
        row = list()
        for j in range(n):
            row.append(float('inf'))
        dist.append(row)
    for i in range(n):
        dist[i][i] = 0
    rates = [0] * n
    visited = [False] * n
    q = deque()
    q.append(graph)
    while len(q):
        node: Node = q.popleft()
        idx = node.id
        visited[idx] = True
        rates[idx] = node.rate
        for neighbor in node.neighbors:
            nidx = neighbor.id
            dist[idx][nidx] = 1
            if not visited[nidx]:
                q.append(neighbor)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist, rates

def dfs(node: int, dist: List[List[int]], rates: List[int], visited: List[bool], time: int, pressure: int, nodes: int, time_limit: int) -> int:
    if time >= time_limit:
        return pressure
    if all(visited):
        return pressure
    visited[node] = True
    # Open this valve
    current_time = time + 1
    current_pressure = (time_limit - time) * rates[node] + pressure
    max_pressure = current_pressure
    # Go to all neighbors via floyd warshall shortest path
    for idx in range(nodes):
        if visited[idx]:
            continue
        sp = dist[node][idx]
        if sp > 0:
            neighbor_time = current_time + sp
            neighbor_pressure = current_pressure
            pressure = dfs(idx, dist, rates, visited.copy(), neighbor_time, neighbor_pressure, nodes, time_limit)
            if pressure > max_pressure:
                max_pressure = pressure
    return max_pressure

def sol1(input_file: Path) -> List[int]:
    entries: List[Tuple[Node, List[str]]] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            node, neighbors = process_line(idx, line)
            entries.append((node, neighbors))
    graph = get_graph(entries)
    n = len(entries)
    dist, rates = floyd_warshall(graph, n)
    visited = [False] * n
    # Valves with rate == 0 do not matter
    for i in range(n):
        if rates[i] == 0:
            visited[i] = True
    # Start opening valve from all nodes assuming first one is AA
    aa_idx = graph.id
    final_pressure = 0
    for idx in range(n):
        if visited[idx]:
            continue
        node, _ = entries[idx]
        if idx == aa_idx:
            time = 1
        else:
            sp = dist[aa_idx][idx]
            if sp == 0:
                continue
            time = 1 + sp
        pressure = dfs(idx, dist, rates, visited.copy(), time, 0, n, 30)
        if pressure > final_pressure:
            final_pressure = pressure
    print(f"Result: {final_pressure}")

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def get_all_subset_combinations(rates: List[int]):
    nodes = set()
    for idx, rate in enumerate(rates):
        if rate != 0:
            nodes.add(idx)
    subsets_person = list(powerset(nodes))
    subsets_elephant = [nodes - set(sp) for sp in subsets_person]
    return subsets_person, subsets_elephant

def sol2(input_file: Path) -> List[int]:
    entries: List[Tuple[Node, List[str]]] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            node, neighbors = process_line(idx, line)
            entries.append((node, neighbors))
    graph = get_graph(entries)
    n = len(entries)
    dist, rates = floyd_warshall(graph, n)
    visited = [False] * n
    # Valves with rate == 0 do not matter
    for i in range(n):
        if rates[i] == 0:
            visited[i] = True
    subsets_person, subsets_elephant = get_all_subset_combinations(rates)
    # Start opening valve from all nodes assuming first one is AA
    aa_idx = graph.id
    final_pressure = 0
    memoization = dict()
    for person, elephant in zip(subsets_person, subsets_elephant):
        if not person or not elephant:
            continue
        person_key = tuple(sorted(person))
        if person_key in memoization:
            person_pressure = memoization[person_key]
        else:
            person_pressure = 0
            visited_person = visited.copy()
            for idx in elephant:
                visited_person[idx] = True
            # Person path
            for idx in person:
                if visited_person[idx]:
                    continue
                node, _ = entries[idx]
                if idx == aa_idx:
                    time = 1
                else:
                    sp = dist[aa_idx][idx]
                    if sp == 0:
                        continue
                    time = 1 + sp
                pressure = dfs(idx, dist, rates, visited_person.copy(), time, 0, n, 26)
                if pressure > person_pressure:
                    person_pressure = pressure
            memoization[person_key] = person_pressure
        # Elephant path
        elephant_key = tuple(sorted(elephant))
        if elephant_key in memoization:
            elephant_pressure = memoization[elephant_key]
        else:
            elephant_pressure = 0
            visited_elephant = visited.copy()
            for idx in person:
                visited_elephant[idx] = True
            for idx in elephant:
                if visited_elephant[idx]:
                    continue
                node, _ = entries[idx]
                if idx == aa_idx:
                    time = 1
                else:
                    sp = dist[aa_idx][idx]
                    if sp == 0:
                        continue
                    time = 1 + sp
                pressure = dfs(idx, dist, rates, visited_elephant.copy(), time, 0, n, 26)
                if pressure > elephant_pressure:
                    elephant_pressure = pressure
            pressure = person_pressure + elephant_pressure
            if pressure > final_pressure:
                final_pressure = pressure
            memoization[elephant_key] = elephant_pressure
    print(f"Result: {final_pressure}")


def test_1_test():
    input_file = Path('2022/16/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/16/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/16/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/16/input.txt')
    result = sol2(input_file)
    print(result)