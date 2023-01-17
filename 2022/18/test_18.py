import pytest
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple, Dict, Set
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict, deque
import re
import json
from enum import Enum
from functools import cmp_to_key
import itertools
import logging

logging.getLogger('matplotlib.font_manager').disabled = True

class Point:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"P({self.x},{self.y},{self.z})"
    def __str__(self):
        return self.__repr__()

def process_line(line: str) -> Point:
    tokens = line.split(',')
    x = int(tokens[0])
    y = int(tokens[1])
    z = int(tokens[2])
    return Point(x,y,z)

class Droplet:
    def __init__(self, points: List[Point]):
        self.points = points
        self.xmax = 0
        self.ymax = 0
        self.zmax = 0
        self.coordinates: Set[Tuple[int,int,int]] = set()
        for point in self.points:
            self.coordinates.add((point.x,point.y,point.z))
            if point.x > self.xmax:
                self.xmax = point.x
            if point.y > self.ymax:
                self.ymax = point.y
            if point.z > self.zmax:
                self.zmax = point.z
    def point_surface(self, point: Point) -> int:
        sides = 0
        x,y,z = point.x, point.y, point.z
        for side in [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]:
            if side in self.coordinates:
                continue
            else:
                sides += 1
        return sides
    def surface(self) -> int:
        total_surface = 0
        for point in self.points:
            surface = self.point_surface(point)
            total_surface += surface
        return total_surface
    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        # Make grid
        voxels = np.zeros((self.xmax + 2, self.ymax + 2, self.zmax + 2))
        for x,y,z in self.coordinates:
            # Activate single Voxel
            voxels[x, y, z] = True

        x,y,z = np.indices(np.array(voxels.shape)+1)

        ax.voxels(x*0.5, y, z, voxels, edgecolor="k")
        ax.set_xlabel('0 - Dim')
        ax.set_ylabel('1 - Dim')
        ax.set_zlabel('2 - Dim')

        plt.show()

class Box:
    def __init__(self, xmax: int, ymax: int, zmax: int):
        self.points: List[Point] = list()
        self.coordinate: Dict[Tuple[int,int,int], int] = dict()
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        for x in range(xmax+1):
            for y in range(ymax+1):
                for z in range(zmax+1):
                    point = Point(x,y,z)
                    self.points.append(point)
                    self.coordinate[(x,y,z)] = 0
    def mark_drop(self, droplet: Droplet):
        for pos in droplet.coordinates:
            self.coordinate[pos] = 1
        pos = (self.xmax, self.ymax, self.zmax)
        self.mark_outside(pos)
    def mark_outside(self, pos: Tuple[int,int,int]):
        x,y,z = pos
        q = deque()
        q.append(pos)
        while len(q):
            pos = q.popleft()
            x,y,z = pos
            if self.coordinate[pos] == 0:
                self.coordinate[pos] = -1
                for npos in [(x+1,y,z),(x-1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z+1),(x,y,z-1)]:
                    nx, ny, nz = npos
                    if nx < 0 or nx > self.xmax or ny < 0 or ny > self.ymax or nz < 0 or nz > self.zmax:
                        continue
                    if self.coordinate[npos] == 0:
                        q.append(npos)
        return
    def get_inside(self) -> Droplet:
        inside_points = list()
        for pos, val in self.coordinate.items():
            if val == 0:
                x,y,z = pos
                point = Point(x,y,z)
                inside_points.append(point)
        inside = Droplet(inside_points)
        return inside

def sol1(input_file: Path) -> List[int]:
    points: List[Point] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            point = process_line(line)
            points.append(point)
    drop = Droplet(points)
    surface = drop.surface()
    print(f"Result: {surface}")
    drop.draw()

def sol2(input_file: Path) -> List[int]:
    points: List[Point] = list()
    with input_file.open('r') as inf:
        for idx, line in enumerate(inf):
            line = line.strip()
            point = process_line(line)
            points.append(point)
    drop = Droplet(points)
    xmax = drop.xmax + 1
    ymax = drop.ymax + 1
    zmax = drop.zmax + 1
    box = Box(xmax, ymax, zmax)
    box.mark_drop(drop)
    inside = box.get_inside()
    drop_surface = drop.surface()
    inside_surface = inside.surface()
    surface = drop_surface - inside_surface
    print(f"Result: {surface}")

def test_1_test():
    input_file = Path('2022/18/test_input.txt')
    result = sol1(input_file)
    print(result)

def test_1_test2():
    input_file = Path('2022/18/test_input2.txt')
    result = sol1(input_file)
    print(result)

def test_1():
    input_file = Path('2022/18/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/18/test_input.txt')
    result = sol2(input_file)
    print(result)

def test_2():
    input_file = Path('2022/18/input.txt')
    result = sol2(input_file)
    print(result)