import pytest
from typing import Optional, List, Tuple
from pathlib import Path
from queue import PriorityQueue
import heapq

def test():
    input_file = Path('2022/1/input.txt')
    elfs = list()
    with input_file.open('r') as inf:
        current_elf = 0
        for line in inf:
            line = line.strip()
            if not line or line == "":
                elfs.append((current_elf, current_elf))
                current_elf = 0
            else:
                current_elf += int(line)
    elfs.append((current_elf,current_elf))
    result = heapq.nlargest(3, elfs)
    values = [value for idx, value in result]
    total = sum(values)
    print(total)