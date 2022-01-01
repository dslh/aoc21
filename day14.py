#!/usr/bin/env python3

from itertools import chain

def pairwise(lst):
    for i in range(1, len(lst)):
        yield lst[i-1:i+1]

# Naive solution, too inefficient for part 2
class Polymizer:
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            base, insert = rule.split(' -> ')
            self.rules[base] = base[0] + insert

    def expand(self, polymer):
        return ''.join(self.rules[pair] for pair in pairwise(polymer)) + polymer[-1]

    def expand_n(self, polymer, steps):
        for _ in range(steps):
            polymer = self.expand(polymer)

        return polymer

def polymer_rating(polymer):
    chars = set(polymer)
    counts = [polymer.count(char) for char in chars]

    return max(counts) - min(counts)

def pair_counts(polymer):
    counts = {pair:0 for pair in pairwise(polymer)}
    for pair in pairwise(polymer):
        counts[pair] += 1
    return counts

def pairwise_rating(pair_counts):
    letter_counts = {}
    for pair,_ in pair_counts:
        letter_counts[pair[0]] = 0
        letter_counts[pair[1]] = 0

    for pair, count in pair_counts:
        letter_counts[pair[0]] += count
        letter_counts[pair[1]] += count

    highest = max(letter_counts, key=letter_counts.get)
    lowest = min(letter_counts, key_letter_counts.get)

    return highest - lowest

# Solution for part 2
class PolymerCounter:
    def __init__(self, rules, polymer):
        self.pair_counts = pair_counts(polymer)
        self.first = polymer[0]
        self.last = polymer[-1]

        self.rules = {}
        for rule in rules:
            base, insert = rule.split(' -> ')
            self.rules[base] = (base[0] + insert, insert + base[1])

        self.pairs = set()
        for (a,b) in self.rules.values():
            self.pairs.add(a)
            self.pairs.add(b)

    def expand(self):
        new_counts = {pair:0 for pair in self.pairs}
        for pair, (a, b) in self.rules.items():
            if pair not in self.pair_counts:
                continue

            new_counts[a] += self.pair_counts[pair]
            new_counts[b] += self.pair_counts[pair]
        self.pair_counts = new_counts

    def expand_n(self, steps):
        for _ in range(steps):
            self.expand()

    def counts(self):
        flatten = chain.from_iterable
        counts = {char:0 for char in flatten(flatten(self.pairs))}

        for (a,b), count in self.pair_counts.items():
            counts[a] += count
            counts[b] += count

        # Every character is counted in two pairs,
        # except the first and last.
        counts[self.first] += 1
        counts[self.last] += 1
        return {char:count//2 for char, count in counts.items()}

    def rating(self):
        counts = self.counts()

        highest = max(counts.values())
        lowest = min(counts.values())

        return highest - lowest

if __name__ == '__main__':
    from get_aoc import get_input_chunks
    base, rules = get_input_chunks(14)
    rules = rules.split('\n')

    polymizer = Polymizer(rules)
    polymer = polymizer.expand_n(base, 10)

    print('Part 1:')
    print(polymer_rating(polymer))

    counter = PolymerCounter(rules, base)
    counter.expand_n(40)

    print('Part 2:')
    print(counter.rating())
