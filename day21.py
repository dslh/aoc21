#!/usr/bin/env python3

def deterministic_die():
    value = 1
    while True:
        yield value
        value %= 100
        value += 1

def play(positions, die):
    players = len(positions)
    scores = [0] * players

    player = 0
    rolls = 0

    while max(scores) < 1000:
        roll = next(die) + next(die) + next(die)
        rolls += 3

        positions[player] = ((positions[player] - 1 + roll) % 10) + 1
        scores[player] += positions[player]

        player = (player + 1) % players

    return sum(score for score in scores if score < 1000) * rolls

if __name__ == '__main__':
    from get_aoc import get_input_lines
    positions = [int(line.split(':')[1]) for line in get_input_lines(21)]

    print('Part 1:')
    print(play(positions, iter(deterministic_die())))
