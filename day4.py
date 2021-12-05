#!/usr/bin/env python3

from get_aoc import get_input_chunks

raw = get_input_chunks(4)

# The numbers to be drawn from the barrel
draw = [int(n) for n in raw[0].split(',')]

# The dimensions of a bingo card
SIZE = 5

# A class representing a bingo card. Stores the numbers on the card, keeps track of which
# ones have been marked, and detects bingo.
class BingoCard:
    # Create a new card from a chunk of text
    def __init__(self, text):
        # The numbers on the card. Stored as a dictionary of number => position for fast lookup
        self.numbers = {int(n):i for i, n in enumerate(text.split())}

        # Set up the list of which numbers have been marked
        self.reset()

        # Flag denoting if the card has achieved bingo
        self.bingo = False

    def reset(self):
        # A list of booleans corresponding to numbers, marking the positions that have been drawn
        self.marked = [False] * len(self.numbers)


    # Reproduce the original text used to generate the card.
    # Makes `print(card)` give a nice output
    def __str__(self):
        rows = [self.numbers[i:i+SIZE] for i in range(0, len(self.numbers), SIZE)]
        return '\n'.join(' '.join(str(n).rjust(2, ' ') for n in row) for row in rows)

    # Mark off a number on the card as it is drawn
    def mark(self, number):
        if number not in self.numbers:
            return
        position = self.numbers[number]

        self.marked[position] = True

        # Check for bingo when a number is marked, that way there is only one row and column to check
        self._check_bingo(position)

    # Check if we have attained bingo, and store the winning number for score calculation
    def _check_bingo(position):
        # Once is enough
        if self.bingo:
            return

        col = position % SIZE
        row_start = position - col

        # All numbers in the row are marked, or all numbers in the column
        self.bingo = all(mark for mark in self.marked[row_start:row_start+SIZE])
                    or all(mark for mark in self.marked[col::SIZE])
        if self.bingo:
            self.winning_number = number

    # As described in the puzzle, a card's score is the sum of the unmarked numbers,
    # multiplied by the last drawn number that created a bingo
    def score(self):
        return sum(n for (n,i) in self.numbers.items() if not self.marked[i]) * self.winning_number

# Read cards from the input
cards = [BingoCard(card) for card in raw[1:]]

def find_winner(draw, cards):
    for number in draw:
        for card in cards:
            card.mark(number)
            if card.bingo:
                return card

winner = find_winner(draw, cards)

print("Part 1:")
print(winner.score())

for card in cards:
    card.reset()

def find_loser(draw, cards):
    winner_count = 0
    card_count = len(cards)
    for number in draw:
        for card in cards:
            card.mark(number)

            if card.bingo:
                winner_count += 1
                if winner_count == card_count:
                    return card

        cards = [card for card in cards if not card.bingo]

    return winner_count

loser = find_loser(draw, cards)

print("Part 2:")
print(loser.score())
