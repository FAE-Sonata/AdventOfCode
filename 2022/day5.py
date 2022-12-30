# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 23:49:16 2022

@author: heyu1
"""
import re
MOVE_RE = re.compile("move \d+ from \d+ to \d+")
BOX_RE = re.compile("^\[[A-Z]\]")

def starting_stacks(filename):
    col_nums = move_start = -1
    with open(filename) as file:
        lines = [line for line in file]
        assert re.match(BOX_RE, lines[0]) is not None
        idx = 0
        for line in lines:
            line = line.strip()
            if col_nums < 0 and re.match(BOX_RE, line) is None:
                col_nums = idx
            if re.match(MOVE_RE, line):
                move_start = idx
                break
            idx += 1
    assert min(col_nums, move_start) > 0
    cols = [int(x) for x in lines[col_nums].strip().split()]
    N_COLS = len(cols)
    assert N_COLS == len(set(cols))
    assert all([cols[k] - cols[k-1] == 1 for k in range(1, N_COLS)])
    LEN_BOX = len("[A] ")
    STANDARD_LEN = N_COLS * LEN_BOX
    assert all([len(line) == STANDARD_LEN for line in lines[:col_nums]])
    stacks = {}
    for line_num in range(col_nums-1, -1, -1):
        for box in cols:
            idx = 1 + LEN_BOX * (box - cols[0])
            this_char = lines[line_num][idx]
            if this_char == " ":
                continue
            if box in stacks:
                stacks[box].append(this_char)
            else:
                stacks[box] = [this_char]
    return stacks, move_start 

ADVENT_INPUT = "C:/HY/Python_exploration/advent_of_code/2022/files/day5.txt"
stacks, move_start = starting_stacks(ADVENT_INPUT)
assert len(stacks[1]) == 8 and (stacks[1][0], stacks[1][-1]) == ("R", "M")
assert len(stacks[2]) == 8 and (stacks[2][0], stacks[2][-1]) == ("P", "H")
assert len(stacks[3]) == 5 and (stacks[3][0], stacks[3][-1]) == ("W", "G")
assert len(stacks[4]) == 3 and stacks[4] == ["N","B","S"]
assert len(stacks[5]) == 8 and (stacks[5][0], stacks[5][-1]) == ("M", "N")

def get_move_info(line):
    assert re.match(MOVE_RE, line)
    idx_from = line.find('from')
    idx_to = line.find('to')
    first_match = re.search("\d+", line)
    origin_match = re.search("\d+", line[idx_from:])
    dest_match = re.search("\d+", line[idx_to:])
    amount = int(first_match[0])
    origin = int(origin_match[0])
    dest = int(dest_match[0])
    return amount, origin, dest

def execute_moves(filename, start):
    with open(filename) as file:
        lines = [line for line in file]
        for k in range(start, len(lines)):
            this_line = lines[k]
            amount, origin, dest = get_move_info(this_line)
            
            assert origin, dest in stacks and amount <= len(stacks[origin])
            removed = stacks[origin][-amount:]
            stacks[origin] = stacks[origin][:-amount]
            removed.reverse()
            stacks[dest].extend(removed)

execute_moves(ADVENT_INPUT, move_start)
NUM_EQS = 10
print("=" * NUM_EQS + "PART I" + "=" * NUM_EQS)
for stack_num, boxes in stacks.items():
    print(f"Stack {stack_num} is topped by {boxes[-1]}")

stacks, move_start = starting_stacks(ADVENT_INPUT)

def execute_moves_preserve_order(filename, start):
    with open(filename) as file:
        lines = [line for line in file]
        for k in range(start, len(lines)):
            this_line = lines[k]
            amount, origin, dest = get_move_info(this_line)
            
            assert origin, dest in stacks and amount <= len(stacks[origin])
            removed = stacks[origin][-amount:]
            stacks[origin] = stacks[origin][:-amount]
            stacks[dest].extend(removed)

execute_moves_preserve_order(ADVENT_INPUT, move_start)
print("=" * NUM_EQS + "PART II" + "=" * NUM_EQS)
for stack_num, boxes in stacks.items():
    print(f"Stack {stack_num} is topped by {boxes[-1]}")