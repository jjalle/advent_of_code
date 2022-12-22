import pytest
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from queue import PriorityQueue
import heapq
from collections import OrderedDict
import re

CD_PATTERN = r'\$ cd (.*)'
LS_PATTERN = r'\$ ls'
DIR_PATTERN = r'dir (.*)'
FILE_PATTERN = r'(\d+) (.*)'

class MyPath:
    def __init__(self):
        self.childs = list()
    def update(self, relative: str):
        if relative == "..":
            self.childs.pop()
        elif relative == "/":
            self.childs = list()
        else:
            self.childs.append(relative)
    def get_parts(self) -> List[str]:
        return self.childs
    def __repr__(self) -> str:
        return '/' + '/'.join(self.childs)
    def __str__(self) -> str:
        return '/' + '/'.join(self.childs)

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
    def add_child(self, child):
        raise RuntimeError(f"TODO")
    def get_child(self, name: str):
        raise RuntimeError(f"TODO")
    def _get_folder(self, path_elements: List[str]):
        raise RuntimeError(f"TODO")
    def compute_size(self) -> int:
        return self.size
    def get_folders_with_lower_size(self, size: int):
        return []
    def get_folders_and_size(self) -> List[Tuple[int, 'Folder']]:
        return []

class Folder:
    def __init__(self, name):
        self.name = name
        self.childs = dict()
        self.size = 0
    def add_child(self, child):
        name = child.name
        self.childs[name] = child
    def get_child(self, name: str):
        return self.childs[name]
    def _get_folder(self, path_elements: List[str]):
        child_name = path_elements[0]
        child = self.childs[child_name]
        if len(path_elements) == 1:
            return child
        else:
            return child._get_folder(path_elements[1:])
    def get_folders_and_size(self) -> List[Tuple[int, 'Folder']]:
        result = list()
        for child in self.childs.values():
            cr = child.get_folders_and_size()
            result.extend(cr)
        result.append((self.size, self))
        return result
    def compute_size(self) -> int:
        size = 0
        for child in self.childs.values():
            cs = child.compute_size()
            size += cs
        self.size = size
        return self.size
    def get_folders_with_lower_size(self, size: int) -> List['Folder']:
        result = list()
        for child in self.childs.values():
            cr = child.get_folders_with_lower_size(size)
            result.extend(cr)
        if self.size <= size:
            result.append(self)
        return result

class FS:
    def __init__(self):
        self.childs = dict()
        self.size = 0
    def add_child(self, child):
        name = child.name
        self.childs[name] = child
    def get_child(self, name: str):
        return self.childs[name]
    def get_folder(self, path: MyPath):
        path_elements = path.get_parts()
        if not path_elements:
            return self
        child_name = path_elements[0]
        child = self.childs[child_name]
        if len(path_elements) > 1:
            return child._get_folder(path_elements[1:])
        else:
            return child
    def compute_size(self) -> int:
        size = 0
        for child in self.childs.values():
            cs = child.compute_size()
            size += cs
        self.size = size
        return self.size
    def get_folders_with_lower_size(self, size: int) -> List[Folder]:
        result = list()
        for child in self.childs.values():
            cr = child.get_folders_with_lower_size(size)
            result.extend(cr)
        if self.size <= size:
            result.append(self)
        return result
    def get_folders_and_size(self) -> List[Tuple[int, 'Folder']]:
        result = list()
        for child in self.childs.values():
            cr = child.get_folders_and_size()
            result.extend(cr)
        result.append((self.size, self))
        return result

class CDCmd:
    def __init__(self, name: str, ):
        pass

def process_command(line: str) -> Tuple[str, int]:
    line.strip()
    match = re.match(CD_PATTERN, line)
    if match:
        child = match.group(1)
        return ("cd", child)
    else:
        match2 = re.match(LS_PATTERN, line)
        if match2:
            return ("ls", None)
        else:
            raise NotImplementedError("")

def process_result(line: str) -> Tuple[str, str, int]:
    line.strip()
    match = re.match(DIR_PATTERN, line)
    if match:
        name = match.group(1)
        return ("dir", name, None)
    else:
        match2 = re.match(FILE_PATTERN, line)
        if match2:
            size = int(match2.group(1))
            name = match2.group(2)
            return ("file", name, size)
        else:
            raise NotImplementedError("")

def sol1(input_file: Path) -> List[int]:
    fs = FS()
    cmd = None
    path = MyPath()
    with input_file.open('r') as inf:
        for line in inf:
            if line.startswith("$"):
                cmd, relpath = process_command(line)
                if cmd == "cd":
                    path.update(relpath)
            else:
                res, name, size = process_result(line)
                if res == "dir":
                    child = Folder(name)
                else:
                    child = File(name, size)
                current_folder = fs.get_folder(path)
                current_folder.add_child(child)
    total_size = fs.compute_size()
    print(f"Total: {total_size}")
    dirs = fs.get_folders_with_lower_size(100000)
    final_size = 0
    for dir in dirs:
        final_size += dir.size
        print(dir.name)
    print(f"Result: {final_size}")

def sol2(input_file: Path) -> List[int]:
    fs = FS()
    cmd = None
    path = MyPath()
    total_space = 70000000
    free_space = 30000000
    with input_file.open('r') as inf:
        for line in inf:
            if line.startswith("$"):
                cmd, relpath = process_command(line)
                if cmd == "cd":
                    path.update(relpath)
            else:
                res, name, size = process_result(line)
                if res == "dir":
                    child = Folder(name)
                else:
                    child = File(name, size)
                current_folder = fs.get_folder(path)
                current_folder.add_child(child)
    total_size = fs.compute_size()
    print(f"Total: {total_size}")
    available = (total_space - total_size)
    if available < free_space:
        to_delete = free_space - available
        folders_and_size = fs.get_folders_and_size()
        folders_and_size.sort(key=lambda entry: entry[0])
        for size, folder in folders_and_size:
            if size >= to_delete:
                print(f"Result: {size} for folder {folder.name}")
                return

def test_1_test():
    input_file = Path('2022/7/test_input.txt')
    results = sol1(input_file)
    print(results)

def test_1():
    input_file = Path('2022/7/input.txt')
    result = sol1(input_file)
    print(result)

def test_2_test():
    input_file = Path('2022/7/test_input.txt')
    results = sol2(input_file)
    print(results)

def test_2():
    input_file = Path('2022/7/input.txt')
    result = sol2(input_file)
    print(result)