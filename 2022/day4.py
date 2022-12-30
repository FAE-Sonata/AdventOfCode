# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 22:05:57 2022

@author: heyu1
"""

def parse_line(line):
    assignments = [[int(num) for num in pair.split("-")] for pair in line.split(",")]
    assignments.sort(key=lambda x: (x[0], x[1]))
    first = assignments[0]; second = assignments[1]
    assert first[0] <= first[1] and second[0] <= second[1]
    return first, second

def fully_contains(line):
    first, second = parse_line(line)
    return second[1] <= first[1] or first[0] == second[0]

def process_day4(filename):
    with open(filename) as file:
        return sum([fully_contains(line.strip()) for line in file])

def any_intersection(line):
    first, second = parse_line(line)
    return first[1] >= second[0]

def process_day4_part2(filename):
    with open(filename) as file:
        return sum([any_intersection(line.strip()) for line in file])

test_cases = ["67-84,66-87", "70-70,40-69", "32-77,31-78", "10-84,11-96",
              "15-95,14-94", "53-55,48-54", "40-92,39-93", "67-91,66-66",
              "74-99,74-98"]
test1 = [fully_contains(s) for s in test_cases]
test2 = [any_intersection(s) for s in test_cases]
assert test1 == [True, False, True, False,
                 False, False, True, False,
                 True]
assert test2 == [True, False, True, True,
                 True, True, True, False,
                 True]

print(process_day4("C:/HY/Python_exploration/advent_of_code/2022/files/day4.txt"))
print(process_day4_part2("C:/HY/Python_exploration/advent_of_code/2022/files/day4.txt"))