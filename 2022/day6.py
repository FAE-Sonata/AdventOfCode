# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 21:44:58 2022

@author: heyu1
"""

from collections import Counter
LOCATION = "C:/HY/Python_exploration/advent_of_code/2022/files"
STANDARD_LEN = 4; LONGER_LEN = 14

def start_of_packet(filename, seq_len):
    with open(filename) as file:
        chars = [line for line in file][0]
        N = len(chars)
        assert N >= seq_len
        window_count = Counter(chars[:seq_len])
        if max(window_count.values()) == 1:
            return seq_len
        for k in range(seq_len, N):
            this_char = chars[k]; prior_char = chars[k - seq_len]
            if this_char == prior_char:
                continue
            if window_count[prior_char] == 1:
                del window_count[prior_char]
            else:
                window_count[prior_char] -= 1
            window_count[this_char] += 1
            if max(window_count.values()) == 1:
                return k + 1
    return -1

assert start_of_packet(f"{LOCATION}/day6-test1.txt", STANDARD_LEN) == 5
assert start_of_packet(f"{LOCATION}/day6-test2.txt", STANDARD_LEN) == 6
assert start_of_packet(f"{LOCATION}/day6-test3.txt", STANDARD_LEN) == 10
assert start_of_packet(f"{LOCATION}/day6-test4.txt", STANDARD_LEN) == 11
print(start_of_packet(f"{LOCATION}/day6.txt", STANDARD_LEN))

print(f"{'='*5} PART II {'='*5}")
assert start_of_packet(f"{LOCATION}/day6-test5.txt", LONGER_LEN) == 19
assert start_of_packet(f"{LOCATION}/day6-test6.txt", LONGER_LEN) == 23
assert start_of_packet(f"{LOCATION}/day6-test7.txt", LONGER_LEN) == 23
assert start_of_packet(f"{LOCATION}/day6-test8.txt", LONGER_LEN) == 29
assert start_of_packet(f"{LOCATION}/day6-test9.txt", LONGER_LEN) == 26
print(start_of_packet(f"{LOCATION}/day6.txt", LONGER_LEN))