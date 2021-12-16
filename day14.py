#!/usr/bin/env python3

def pairwise(lst):
    for i in range(1, len(lst)):
        yield lst[i-1:i+1]

def _parse_rule(rule):
    base, insert = rule.split(' -> ')
    return base, (base[0] + insert)

class Polymizer:
    def __init__(self, rules):
        self.rules = dict(_parse_rule(rule) for rule in rules)

    def expand(self, polymer):
        return ''.join(self.rules[pair] for pair in pairwise(polymer)) + polymer[-1]

    def expand_n(self, polymer, steps):
        analyse(polymer)
        for _ in range(steps):
            polymer = self.expand(polymer)
            analyse(polymer)

        return polymer

    def analysis(self, polymer, steps):
        analysis = []
        for _ in range(steps):
            polymer = self.expand(polymer)
            analysis.append({char:polymer.count(char) for char in sorted(set(polymer))})

        return analysis

def polymer_rating(polymer):
    chars = set(polymer)
    counts = [polymer.count(char) for char in chars]

    return max(counts) - min(counts)

def analyse(polymer):
    for char in sorted(set(polymer)):
        print(f"{char}:{polymer.count(char)}", end="\t")
    print()

if __name__ == '__main__':
    from get_aoc import get_input_chunks
    base, rules = get_input_chunks(14)

    polymizer = Polymizer(rules.split('\n'))
    polymer = polymizer.expand_n(base, 10)

    print('Part 1:')
    print(polymer_rating(polymer))

    polymer = polymizer.expand_n(base, 40)
    print('Part 2:')
    print(polymer_rating(polymer))
