# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 18:49:30 2022

@author: heyu1
"""

ROCK_ORD = [ord("A"), ord("X")]
"""
rock = 0, paper = 1, scissors = 2
paper counters rock (1 vs 0),
scissors counters paper (2 vs 1)
rock counters scissors (0 vs 2)
Thus, if
1. CODE_SELF = ((CODE_OPPONENT + 1) % 3), self wins
2. CODE_SELF = ((CODE_OPPONENT - 1) % 3), self loses
3. CODE_SELF == CODE_OPPONENT, DRAW
"""
def score_line(opponent_code, own_code):
    battle = 3 if opponent_code == own_code else 6 * (own_code == (
        (opponent_code + 1) % 3))
    return (1 + own_code) + battle

def process_day2(filename):
    res = 0
    with open(filename) as file:
        for line in file:
            entries = line.split()
            res += score_line(ord(entries[0]) - ROCK_ORD[0],
                              ord(entries[1]) - ROCK_ORD[1])
    return res

"""
Part 2: X = lose, Y = draw, Z = win
"""
def score_line_part2(opponent_code, own_code):
    own_shape = (opponent_code + (own_code - 1)) % 3
    return (1 + own_shape) + (3 * own_code)

def process_day2_part2(filename):
    res = 0
    with open(filename) as file:
        for line in file:
            entries = line.split()
            res += score_line_part2(ord(entries[0]) - ROCK_ORD[0],
                                    ord(entries[1]) - ROCK_ORD[1])
    return res

print(process_day2("C:/HY/Python_exploration/advent_of_code/2022/files/day2.txt"))
print(process_day2_part2("C:/HY/Python_exploration/advent_of_code/2022/files/day2.txt"))