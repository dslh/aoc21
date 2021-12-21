#!/usr/bin/env python3

def deterministic_die():
    value = 1
    while True:
        yield value
        value %= 100
        value += 1

def play_deterministic(positions):
    players = len(positions)
    scores = [0] * players

    player = 0
    rolls = 0
    die = 0

    while max(scores) < 1000:
        roll = die * 3 + 6
        die += 3
        die %= 100
        rolls += 3

        positions[player] = ((positions[player] - 1 + roll) % 10) + 1
        scores[player] += positions[player]

        player = (player + 1) % players

    return sum(score for score in scores if score < 1000) * rolls

# Distribution when rolling three three-sided dice
ROLL_DISTRIBUTION = {
    (3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)
}

class Game:
    def __init__(self, positions, scores, turn):
        self.positions = positions
        self.scores = scores
        self.turn = turn

    def play(self, roll):
        positions = self.positions.copy()
        scores = self.scores.copy()
        positions[self.turn] = ((positions[self.turn] - 1 + roll) % 10) + 1
        scores[self.turn] += positions[self.turn]

        return Game(positions, scores, (self.turn + 1) % 2)

    def won(self):
        if self.scores[0] >= 21:
            return Wins(1, 0)
        elif self.scores[1] >= 21:
            return Wins(0, 1)

class Wins:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        return Wins(self.a + other.a, self.b + other.b)

    def __mul__(self, scalar):
        return Wins(self.a * scalar, self.b * scalar)

    def tuple(self):
        return (self.a, self.b)

def count_wins(game):
    won = game.won()
    if won: return won

    return sum((count_wins(game.play(roll)) * freq for roll, freq in ROLL_DISTRIBUTION), Wins(0, 0))

def play_quantum(positions):
    return count_wins(Game(positions, [0,0], 0)).tuple()

if __name__ == '__main__':
    from get_aoc import get_input_lines
    positions = [int(line.split(':')[1]) for line in get_input_lines(21)]

    print('Part 1:')
    print(play_deterministic(positions.copy()))

    print('Part 2:')
    print(max(play_quantum(positions)))
