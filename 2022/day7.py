# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 22:26:29 2022

@author: heyu1
"""
import re
LS_RE = re.compile("^\$ ls$")
CD_RE = re.compile("^\$ cd (\w+|\/|\.{2})$")
DIR_RE = re.compile("^dir \w+$")
SIZE_RE = re.compile("^\d+ \w+(\.[A-z]+)?$")
LEN_FRONT = len("$ cd ")
LEN_DIR = len("dir ")
LOCATION = "C:/HY/Python_exploration/advent_of_code/2022/files"
SIZE_LIMIT = 1E5
DISK_SIZE = 7E7
MIN_UNUSED = 3E7

class directory:
    def __init__(self, name="", parent = None):
        assert (parent is None) == (len(name) == 0)
        self.is_root = parent is None
        self.name = name
        self.parent = parent
        self.files = {}
        self.children = {}
    
    def get_is_root(self):
        return self.is_root
    
    def get_name(self):
        return self.name
    
    def get_parent(self):
        return self.parent
    
    def get_top_level_file_size(self):
        return sum(self.files.values())
    
    def get_total_size(self):
        top_level = self.get_top_level_file_size()
        subdir_size = 0
        for subdir_name in self.get_child_names():
            subdir = self.get_child_with_name(subdir_name)
            subdir_size += subdir.get_total_size()
        return top_level + subdir_size
        # return raw_total if raw_total <= limit else 0
    
    def add_single_file(self, name, size):
        assert not(name in self.files)
        self.files[name] = size
    
    def add_multiple_files(self, file_dict):
        existing_keys = set(self.files.keys())
        new_keys = set(file_dict.keys())
        assert len(new_keys.intersection(existing_keys)) == 0
        self.files |= file_dict
    
    def add_single_child(self, new_directory):
        new_name = new_directory.get_name()
        assert not(self.has_child(new_name))
        self.children[new_name] = new_directory
    
    def add_children(self, new_directories):
        new_names = [directory.get_name() for directory in new_directories]
        assert not(new_names in self.children)
        addition = dict(zip(new_names, new_directories))
        self.children |= addition
    
    def get_child_names(self):
        return self.children.keys()
    
    def has_child(self, name):
        return name in self.children
    
    def get_child_with_name(self, name):
        assert self.has_child(name)
        return self.children[name]

def process_terminal_output(filename):
    with open(filename) as file:
        terminal_output = [line.strip() for line in file]
        assert terminal_output[0] == "$ cd /"
        root = directory(); trav = root
        directories = []
        N = len(terminal_output)
        commands = [k for k in range(N) if re.match(LS_RE, terminal_output[k]) or 
                    re.match(CD_RE, terminal_output[k])]
        NUM_COMMANDS = len(commands)
        for k in range(1, NUM_COMMANDS):
            this_line_num = commands[k]
            if this_line_num == N-1:
                break
            upper_limit = N if k == NUM_COMMANDS - 1 else commands[k+1]
            this_line = terminal_output[commands[k]]
            if re.match(CD_RE, this_line):
                assert upper_limit == this_line_num + 1 # cd must be followed by another cd or ls
                if this_line[-2:] == "." * 2:
                    if trav.get_is_root():
                        continue
                    trav = trav.get_parent()
                elif this_line[-1] == "/":
                    trav = root
                else:
                    trav = trav.get_child_with_name(this_line[LEN_FRONT:])
            else:
                assert upper_limit > this_line_num + 1
                for line_num in range(this_line_num+1, upper_limit):
                    info_line = terminal_output[line_num]
                    is_dir = re.match(DIR_RE, info_line)
                    is_file = re.match(SIZE_RE, info_line)
                    assert is_dir or is_file
                    if is_dir:
                        new_dir = directory(info_line[LEN_DIR:], trav)
                        directories.append(new_dir)
                        trav.add_single_child(new_dir)
                    else:
                        size_str = re.match("^\d+" , info_line)[0]
                        file_name = info_line[(len(size_str) + 1):]
                        trav.add_single_file(file_name, int(size_str))
        return root, directories

def part1(filename):
    _, directories = process_terminal_output(filename)
    res = 0
    for subdir in directories:
        size = subdir.get_total_size()
        if size > SIZE_LIMIT:
            continue
        res += size
    return res

def part2(filename):
    root, directories = process_terminal_output(filename)
    MAX_USABLE = DISK_SIZE - MIN_UNUSED
    total_used = root.get_total_size()
    if total_used <= MAX_USABLE:
        return 0
    NEED_TO_FREE = total_used - MAX_USABLE
    sizes = [subdir.get_total_size() for subdir in directories]
    sizes.append(total_used)
    ok_sizes = [size for size in sizes if size >= NEED_TO_FREE]
    ok_sizes.sort()
    return ok_sizes[0]

assert part1(f"{LOCATION}/day7-test.txt") == 95437
print(part1(f"{LOCATION}/day7.txt"))
print(part2(f"{LOCATION}/day7.txt"))