# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 16:39:45 2022

@author: heyu1
"""
import numpy as np

LOCATION = "C:/HY/Python_exploration/advent_of_code/2022/files"

def visible_row_wise(grid, row_num):
    num_rows = len(grid)
    assert row_num >= 0 and row_num < num_rows
    num_cols = len(grid[0])
    if row_num == 0 or row_num == num_rows-1:
        return [True] * num_cols
    res = [False] * num_cols
    res[0] = True; res[-1] = True
    left_max = grid[row_num][0]; right_max = grid[row_num][-1]
    for k in range(1, num_cols - 1):
        left_height = grid[row_num][k]
        right_idx = (num_cols - 1) - k
        right_height = grid[row_num][right_idx]
        if left_height > left_max:
            left_max = left_height
            res[k] = True
        if right_height > right_max:
            right_max = right_height
            res[right_idx] = True
    return res

def visible_col_wise(grid, col_num):
    num_cols = len(grid[0])
    assert col_num >= 0 and col_num < num_cols
    num_rows = len(grid)
    if col_num == 0 or col_num == num_cols-1:
        return [True] * num_rows
    res = [False] * num_rows
    res[0] = True; res[-1] = True
    up_max = grid[0][col_num]; down_max = grid[-1][col_num]
    for k in range(1, num_rows - 1):
        up_height = grid[k][col_num]
        down_idx = (num_rows - 1) - k
        right_height = grid[down_idx][col_num]
        if up_height > up_max:
            up_max = up_height
            res[k] = True
        if right_height > down_max:
            down_max = right_height
            res[down_idx] = True
    return res

def count_visible_trees(grid):
    rows = [visible_row_wise(grid, k) for k in range(len(grid))]
    untransposed = np.array([visible_col_wise(grid, k) for k in range(len(grid[0]))])
    cols = np.transpose(untransposed)
    return sum(sum(rows | cols))

def grade_location(grid, row, col):
    num_rows = len(grid); num_cols = len(grid[0])
    if row == 0 or row == num_rows - 1 or col == 0 or col == num_cols - 1:
        return 0
    this_num = grid[row][col]
    left = np.where([grid[row][k] >= this_num for k in range(col)])[0]
    left_score = col if len(left) == 0 else col - left.max()
    
    right = np.where([grid[row][k] >= this_num for k in range(col+1, num_cols)])[0]
    right_score = (num_cols-1) - col if len(right) == 0 else right.min() + 1#- col
    
    up = np.where([grid[k][col] >= this_num for k in range(row)])[0]
    up_score = row if len(up) == 0 else row - up.max()
    
    down = np.where([grid[k][col] >= this_num for k in range(row+1, num_rows)])[0]
    down_score = (num_rows-1) - row if len(down) == 0 else down.min() + 1# - row
    return left_score * right_score * up_score * down_score

def optimal_score(dimension):
    optimal_location = (dimension >> 1) if dimension % 2 else ((dimension - 1) >> 1)
    return optimal_location * (dimension - 1 - optimal_location)

def best_score(grid):
    num_rows = len(grid); num_cols = len(grid[0])
    theory_max = optimal_score(num_rows) * optimal_score(num_cols)
    res = 0
    for j in range(1, num_rows-1):
        for k in range(1, num_cols-1):
            this_score = grade_location(grid, j, k)
            if this_score == theory_max:
                return theory_max
            res = max(res, this_score)
    return res

def read_grid(filename):
    with open(filename) as file:
        grid = [[int(s) for s in line.strip()] for line in file]
        return grid

test_grid = read_grid(f"{LOCATION}/day8-test.txt")
assert visible_row_wise(test_grid, 0) == [True] * 5
assert visible_row_wise(test_grid, 1) == [True] * 3 + [False, True]
assert visible_row_wise(test_grid, 2) == [True] * 2 + [False] + [True] * 2
assert visible_row_wise(test_grid, 3) == [True, False] * 2 + [True]
assert visible_row_wise(test_grid, 4) == [True] * 5

assert count_visible_trees(test_grid) == 21
advent_grid = read_grid(f"{LOCATION}/day8.txt")
print(count_visible_trees(advent_grid))

assert best_score(test_grid) == 8
print(best_score(advent_grid))