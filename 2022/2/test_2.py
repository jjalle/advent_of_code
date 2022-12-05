import pytest
from typing import Optional, List, Tuple
from pathlib import Path
from queue import PriorityQueue
import heapq

game_result = {
    # Rock vs Rock
    ('A','X'): 1 + 3,
    # Paper vs Rock
    ('B','X'): 1 + 0,
    # Scissors vs Rock
    ('C','X'): 1 + 6,
    # Rock vs Paper
    ('A','Y'): 2 + 6,
    # Paper vs Paper
    ('B','Y'): 2 + 3,
    # Scissors vs Paper
    ('C','Y'): 2 + 0,
    # Rock vs Scissors
    ('A','Z'): 3 + 0,
    # Paper vs Scissors
    ('B','Z'): 3 + 6,
    # Scissors vs Scissors
    ('C','Z'): 3 + 3,
}

game_result2 = {
    # Rock Paper lose:
    ('A','X'): 3 + 0,
    # Paper Rock lose
    ('B','X'): 1 + 0,
    # Scissors Paper lose
    ('C','X'): 2 + 0,
    # Rock Rock draw
    ('A','Y'): 1 + 3,
    # Paper Paper draw
    ('B','Y'): 2 + 3,
    # Scissors Scissors draw
    ('C','Y'): 3 + 3,
    # Rock Paper win
    ('A','Z'): 2 + 6,
    # Paper Scissor win
    ('B','Z'): 3 + 6,
    # Scissors Rock win
    ('C','Z'): 1 + 6,
}

def test_1():
    input_file = Path('2022/2/input.txt')
    result = 0
    with input_file.open('r') as inf:
        for line in inf:
            values = line.strip().split(' ')
            oponent = values[0]
            player = values[1]
            points = game_result[(oponent, player)]
            result += points
    print(result)

def test_2():
    input_file = Path('2022/2/input.txt')
    result = 0
    with input_file.open('r') as inf:
        for line in inf:
            values = line.strip().split(' ')
            oponent = values[0]
            player = values[1]
            points = game_result2[(oponent, player)]
            result += points
    print(result)