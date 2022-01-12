#!/usr/bin/env python3

import operator

VARS = set('wxyz')
class Registry:
    def __init__(self):
        self.ram = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    def eval(self, val):
        if val in VARS:
            return self.ram[val]
        else:
            return int(val)

    def __getitem__(self, var):
        return self.ram[var]

    def set(self, var, val):
        self.ram[var] = val

    def op(self, op, var, val):
        a = self.ram[var]
        b = self.eval(val)
        self.ram[var] = op(a, b)

OPS = {
    'add': operator.add,
    'div': operator.floordiv,
    'eql': operator.eq,
    'mul': operator.mul,
    'mod': operator.mod
}

class Program:
    def __init__(self, lines):
        self.instructions = [line.split() for line in lines]

    def run(self, seq):
        seq = iter(seq)
        registry = Registry()
        for inst in self.instructions:
            if inst[0] == 'inp':
                registry.set(inst[1], next(seq))
            else:
                registry.op(OPS[inst[0]], inst[1], inst[2])

        return registry

def down_counter(digits, value=[]):
    if digits == 0:
        yield value
    else:
        for i in range(9,0,-1):
            val = value + [i]
            yield from down_counter(digits - 1, val)

def accumulate(div, add_x, add_y, w, z):
    x = (z % 26) + add_x
    if div:
        z //= 26

    if x != w:
        z *= 26
        z += w + add_y

    return z

ARGS = [
    (False, 11,  8),
    (False, 12,  8),
    (False, 10, 12),
    (True,  -8, 10),
    (False, 15,  2),
    (False, 15,  8),
    (True, -11,  4),
    (False, 10,  9),
    (True,  -3, 10),
    (False, 15,  3),
    (True,  -3,  7),
    (True,  -1,  7),
    (True, -10,  2),
    (True, -16,  2)
]

from functools import partial
PROGRAM = [partial(accumulate, *args) for args in ARGS]

def find_inputs(args, expected):
    for w in range(9, 0, -1):
        for z in range(expected * 26, (expected + 1) * 26):
            if accumulate(*args, w, z) == expected:
                yield (w, z)

        for z in range(expected, expected + 26):
            if accumulate(*args, w, z) == expected:
                yield (w, z)

        for z in range(expected // 26, (expected // 26) + 26):
            if accumulate(*args, w, z) == expected:
                yield (w, z)

def find_serials(step, expected, serial):
    if step == len(ARGS):
        print(step, expected, serial)

    if step > len(ARGS):
        yield serial
        return

    for w, z in find_inputs(ARGS[-step], expected):
        yield from find_serials(step + 1, z, serial + w * 10 ** (step - 1))

def find_all_serials():
    yield from find_serials(1, 0, 0)

def run(seq):
    z = 0
    for func, w in zip(PROGRAM, seq):
        z = func(w, z)
    return z

if __name__ == '__main__':
    print("Part 1:")
    print(next(find_all_serials()))
