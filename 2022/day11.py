# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 21:32:43 2022

@author: heyu1
"""
import re
LOCATION = "C:/HY/Python_exploration/advent_of_code/2022/files"
# MAX_INT = (1<<31) - 1
LINES_PER_MONKEY = 6
RELIEF = 3
LEN_MONKEY = len("monkey ")
MONKEY_RE = re.compile("^Monkey \d+:$")
START_RE = re.compile("^Starting items: \d+(, \d+)*$")
OP_RE = re.compile("^Operation: new = old (\*|\+) (\d+|old)*$")
ARITH_RE = re.compile("(\*|\+)")
TEST_RE = re.compile("^Test: divisible by \d+$")
TRUE_RE = re.compile("^If true: throw to monkey \d+$")
FALSE_RE = re.compile("^If false: throw to monkey \d+$")

def parse_items(line):
    assert re.match(START_RE, line)
    idx_colon = line.index(":")
    return [int(x) for x in line[(idx_colon+2):].split(",")]

def parse_operation(line):
    assert re.match(OP_RE, line)
    operand = re.search(ARITH_RE, line)[0]
    idx_operand = line.index(operand)
    second = line[(idx_operand+2):]
    return [1 + (operand == "*"), int(second)] if second.isnumeric() else [3]

def parse_divisibility(lines, monkey_idx):
    assert re.match(TEST_RE, lines[0])
    assert re.match(TRUE_RE, lines[1])
    assert re.match(FALSE_RE, lines[2])
    idx_by = lines[0].index("by ")
    idx_monkey1 = lines[1].index("m")
    divisible = [lines[0][(idx_by + len("by ")):],
                 lines[1][(idx_monkey1 + LEN_MONKEY):],
                 lines[2][(idx_monkey1 + LEN_MONKEY + 1):]]
    res = [int(x) for x in divisible]
    assert all([k != monkey_idx for k in res[1:]])
    return res

def parse_rules(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file if len(line.strip()) > 0]
        items = []
        operations = [] # 1 is addition, 2 multiplication by constant, 3 squaring
        divisibility_rules = []
        num_lines = len(lines)
        assert num_lines % LINES_PER_MONKEY == 0
        num_monkeys = num_lines // LINES_PER_MONKEY
        for k in range(num_monkeys):
            header = LINES_PER_MONKEY * k
            # header
            assert re.match(MONKEY_RE, lines[header])
            assert int(lines[header][LEN_MONKEY:-1]) == k
            items.append(parse_items(lines[header+1]))
            operations.append(parse_operation(lines[header+2]))
            
            idx_div = header+3
            divisibility_rules.append(parse_divisibility(
                lines[idx_div:(idx_div+3)], k))
        return items, operations, divisibility_rules

def process_operation(level, operation_info):
    operand = operation_info[0]
    if operand == 3:
        level **= 2
    elif operand == 2:
        level *= operation_info[1]
    else:
        level += operation_info[1]
    return level

def signal_strengths_part1(filename, num_rounds=20, relief=3):
    assert isinstance(num_rounds, int) and num_rounds > 0
    assert isinstance(relief, int) and relief > 1
    items, operations, divisibility_rules = parse_rules(filename)
    N = len(items)
    assert len(operations) == N and len(divisibility_rules) == N
    process_counts = [0] * N
    for k in range(num_rounds):
        for monkey in range(N):
            previous_items = len(items[monkey])
            process_counts[monkey] += previous_items
            for worry_level in items[monkey]:
                level = process_operation(worry_level, operations[monkey])
                level //= relief
                if level % divisibility_rules[monkey][0] == 0:
                    items[divisibility_rules[monkey][1]].append(level)
                else:
                    items[divisibility_rules[monkey][2]].append(level)
            items[monkey] = items[monkey][previous_items:]
    process_counts.sort(reverse=True)
    return process_counts[0] * process_counts[1]

def euclid_gcd(p, q):
    assert p and q, "neither can be zero"
    assert isinstance(p, int) and isinstance(q, int), "must be ints"
    p = abs(p); q = abs(q)
    a = max(p, q); b = min(p, q)
    while b:
        remainder = a % b
        if remainder == 0:
            return b
        a = b; b = remainder
    return b

def lcm(p, q):
    return (p * q) // euclid_gcd(p, q)

def signal_strengths_part2(filename, num_rounds=int(1E4)):
    assert isinstance(num_rounds, int) and num_rounds > 0
    items, operations, divisibility_rules = parse_rules(filename)
    N = len(items)
    assert len(operations) == N and len(divisibility_rules) == N
    monkey_lcm = 1
    for rule in divisibility_rules:
        monkey_lcm = lcm(monkey_lcm, rule[0])
    process_counts = [0] * N
    print("=" * 3 + "BEGIN RUN" + "=" * 3)
    for k in range(num_rounds):
        for monkey in range(N):
            previous_items = len(items[monkey])
            process_counts[monkey] += previous_items
            for worry_level in items[monkey]:
                level = process_operation(worry_level, operations[monkey])
                modulo = level % monkey_lcm
                level = monkey_lcm if modulo == 0 else modulo
                base = divisibility_rules[monkey][0]
                if level % base == 0:
                    items[divisibility_rules[monkey][1]].append(level)
                else:
                    items[divisibility_rules[monkey][2]].append(level)
            items[monkey] = items[monkey][previous_items:]
        if k % 1000 == 999:
            print(f"After round {k+1}: {process_counts}")
    process_counts.sort(reverse=True)
    return process_counts[0] * process_counts[1]
    
assert signal_strengths_part1(f"{LOCATION}/day11-test.txt") == 10605
print(signal_strengths_part1(f"{LOCATION}/day11.txt"))

assert signal_strengths_part2(f"{LOCATION}/day11-test.txt") == 2713310158
print(signal_strengths_part2(f"{LOCATION}/day11.txt"))