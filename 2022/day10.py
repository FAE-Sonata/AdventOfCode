# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 15:45:09 2022

@author: heyu1
"""
import re
INSTRUCTION_RE = re.compile("^(addx|noop)( \-?\d+)?$")
LOCATION = "C:/HY/Python_exploration/advent_of_code/2022/files"
CRT_WIDTH = 40

def parse_instruction(line):
    num_cycle = 1 + (line[:4] == "addx")
    offset = 0
    if num_cycle == 2:
        idx_space = line.index(" ")
        offset = int(line[(idx_space+1):])
    return num_cycle, offset

def signal_strengths_part1(filename, register_start=1):
    res = 0
    cycle_count = 0; level_idx = 0
    register_value = register_start
    LEVELS = [20] + [60 + 40 * x for x in range(5)]
    with open(filename) as file:
        for line in file:
            if cycle_count >= LEVELS[-1]:
                break
            next_level = LEVELS[level_idx]
            line = line.strip()
            assert re.match(INSTRUCTION_RE, line)
            num_cycle, offset = parse_instruction(line)
            if cycle_count < next_level and cycle_count + num_cycle >= next_level:
                res += next_level * register_value
                level_idx += 1
            cycle_count += num_cycle
            register_value += offset
    return res

def get_sprite_position(register):
    modded = register % CRT_WIDTH
    if modded == 0:
        return (0,1)
    if modded == CRT_WIDTH - 1:
        return (CRT_WIDTH - 2, CRT_WIDTH - 1)
    return (modded-1, modded+1)

def signal_strengths_part2(filename, register_start=1):
    assert register_start >= 0 and register_start < CRT_WIDTH
    register_value = register_start; cycle_count = 0
    aligns = []
    with open(filename) as file:
        for line in file:
            sprite = get_sprite_position(register_value)
            line = line.strip()
            assert re.match(INSTRUCTION_RE, line)
            num_cycle, offset = parse_instruction(line)
            for cycle in range(num_cycle):
                crt_position = len(aligns) % CRT_WIDTH
                aligns.append(crt_position >= sprite[0] and crt_position <=
                              sprite[1])
            cycle_count += num_cycle
            register_value += offset
    pixels = ["#" if b else "." for b in aligns]
    pixel_rows = ["".join(pixels[(k-CRT_WIDTH):k]) for k in range(
        CRT_WIDTH, len(pixels) + 1, CRT_WIDTH)]
    return pixel_rows

assert signal_strengths_part1(f"{LOCATION}/day10-test.txt") == 13140
print(signal_strengths_part1(f"{LOCATION}/day10.txt"))

test_rows = signal_strengths_part2(f"{LOCATION}/day10-test.txt")
def part2_test_repeat(N, groups):
    assert N > 1 and groups > 0
    return ('#' * N + '.' * N) * groups
assert test_rows == [
    part2_test_repeat(2, 10), 
    part2_test_repeat(3, 6) + '#' * 3 + '.',
    part2_test_repeat(4, 5),
    part2_test_repeat(5, 4),
    part2_test_repeat(6, 3) + '#' * 4,
    part2_test_repeat(7, 2) + '#' * 7 + '.' * 5
]

letter_rows = signal_strengths_part2(f"{LOCATION}/day10.txt")
for row in letter_rows:
    print(row)