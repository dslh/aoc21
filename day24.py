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

def program(seq):
    seq = iter(seq)
    w = next(seq)
    x = 1
    y = 26
    z = 0

if __name__ == '__main__':
    from get_aoc import get_input_lines

    program = Program(get_input_lines(24))

    print('Part 1:')
    for seq in down_counter(14):
        r = program.run(seq)
        if r['z'] == 0:
            print(seq)
            break
