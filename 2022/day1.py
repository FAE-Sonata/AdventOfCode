# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 17:20:01 2022

@author: heyu1
"""
# import requests

# address = "https://adventofcode.com/2022/day/1/input"
def process_day1(filename):
    res = 0
    with open(filename) as file:
        elf_total = 0
        for line in file:
            if len(line.strip()) == 0:
                res = max(res, elf_total)
                elf_total = 0
            else:
                elf_total += int(line)
        res = max(res, elf_total)
    return res
    # advent_req = requests.get("https://adventofcode.com/2022/day/1/input")

def process_day1_part2(filename):
    res = [0] * 3
    def cycle(arr, new_value):
        replace_idx = -1
        for k, val in enumerate(arr):
            if new_value > val:
                replace_idx = k
                break
        if replace_idx == 2:
            arr[2] = new_value
        elif replace_idx == 1:
            arr[1], arr[2] = new_value, arr[1]
        else:
            arr = [new_value] + arr[:2]
        return arr
            
    with open(filename) as file:
        elf_total = 0
        for line in file:
            if len(line.strip()) == 0:
                if elf_total > min(res):
                    res = cycle(res, elf_total)
                elf_total = 0
            else:
                elf_total += int(line)
        if elf_total > min(res):
            res = cycle(res, elf_total)
    return sum(res)

print(process_day1("C:/HY/Python_exploration/advent_of_code/2022/files/day1.txt"))
print(process_day1_part2("C:/HY/Python_exploration/advent_of_code/2022/files/day1.txt"))