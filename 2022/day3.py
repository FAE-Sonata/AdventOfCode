# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 21:31:28 2022

@author: heyu1
"""

PRIORITY_LOOKUP = [1 - ord("a"), 27 - ord("A")]
def score_item(letter):
    return ord(letter) + PRIORITY_LOOKUP[1] if letter.isupper() else (
        ord(letter) + PRIORITY_LOOKUP[0])

def priority_line(s):
    N = len(s)
    assert N % 2 == 0
    mid = N >> 1
    front = set(s[:mid]); back = set(s[mid:])
    rucksack_duplicate = front.intersection(back)
    assert len(rucksack_duplicate) == 1
    item = (list(rucksack_duplicate))[0]
    return score_item(item)

def process_day3(filename):
    with open(filename) as file:
        return sum([priority_line(line.strip()) for line in file])

def priority_trio_lines(trio):
    assert len(trio) == 3
    common = set(trio[0])
    for line in trio[1:]:
        common = common.intersection(set(line))
    assert len(common) == 1
    item = (list(common))[0]
    return score_item(item)

def process_day3_part2(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
        N = len(lines)
        assert N % 3 == 0
        return sum([priority_trio_lines(lines[k:(k+3)]) for k in range(0, N, 3)])

print(process_day3("C:/HY/Python_exploration/advent_of_code/2022/files/day3.txt"))
print(process_day3_part2("C:/HY/Python_exploration/advent_of_code/2022/files/day3.txt"))