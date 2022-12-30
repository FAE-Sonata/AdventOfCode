# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 19:38:04 2022

@author: heyu1
"""
import re

LOCATION = "C:/HY/Python_exploration/advent_of_code/2022/files"
STEP_RE = re.compile("^[U|R|D|L] \d+$")
DIR_MAP = {"U": (0,1), "R": (1,0), "D": (0,-1), "L": (-1,0)}
LEN_DIR = len("U ")

def update_location(location, vector):
    return (location[0] + vector[0], location[1] + vector[1])

def sign(x):
    return x // abs(x)

def correct_tail(new_h, old_t):
    delta_x = new_h[0] - old_t[0]; delta_y = new_h[1] - old_t[1]
    if abs(delta_x) <= 1 and abs(delta_y) <= 1:
        return old_t
    if delta_x == 0:
        return (new_h[0], old_t[1] + sign(delta_y))
    if delta_y == 0:
        return (old_t[0] + sign(delta_x), new_h[1])
    # diagonal movement required
    return (old_t[0] + sign(delta_x), old_t[1] + sign(delta_y))

def parse_line(line):
    line = line.strip()
    assert re.match(STEP_RE, line)
    return DIR_MAP[line[0]], int(line[LEN_DIR:])

def count_positions_part1(filename, start=(0,0)):
    front = start; rear = start
    visited = set({start})
    with open(filename) as file:
        for line in file:
            direction, steps = parse_line(line)
            for step in range(1, steps+1):
                front = update_location(front, direction)
                rear = correct_tail(front, rear)
                visited.add(rear)
    return len(visited)

def count_positions_part2(filename, ropes=10, start=(0,0)):
    assert ropes > 1
    snake = [start] * ropes
    visited = set({start})
    with open(filename) as file:
        for line in file:
            direction, steps = parse_line(line)
            for step in range(1, steps+1):
                snake[0] = update_location(snake[0], direction)
                for k in range(1, ropes):
                    snake[k] = correct_tail(snake[k-1], snake[k])
                visited.add(snake[-1])
    return len(visited)

assert correct_tail((-2,0), (0,0)) == (-1,0) # W
assert correct_tail((2,0), (0,0)) == (1,0) # E
assert correct_tail((0,2), (0,0)) == (0,1) # N
assert correct_tail((0,-2), (0,0)) == (0,-1) # S
assert correct_tail((4,2), (3,0)) == (4,1) # NE
assert correct_tail((2,4), (4,3)) == (3,4) # NW
assert correct_tail((1,2), (2,4)) == (1,3) # SW
assert correct_tail((4,3), (2,4)) == (3,3) # SE

assert count_positions_part1(f"{LOCATION}/day9-test.txt") == 13
print(count_positions_part1(f"{LOCATION}/day9.txt"))

assert count_positions_part2(f"{LOCATION}/day9-test.txt") == 1
assert count_positions_part2(f"{LOCATION}/day9-test2.txt") == 36
print(count_positions_part2(f"{LOCATION}/day9.txt"))