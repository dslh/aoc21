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

    # Clear the marks on the card, in order to play a new game
    def reset(self):
        # A list of booleans corresponding to numbers, marking the positions that have been drawn
        self.marked = [False] * len(self.numbers)

    # Mark off a number on the card as it is drawn
    def mark(self, number):
        if number not in self.numbers:
            return
        position = self.numbers[number]

        self.marked[position] = True

        # Check for bingo when a number is marked, that way there is only one row and column to check
        # Once is enough
        if self.bingo:
            return

        col = position % SIZE
        row_start = position - col

        # All numbers in the row are marked, or all numbers in the column
        self.bingo = all(mark for mark in self.marked[row_start:row_start+SIZE]) or all(mark for mark in self.marked[col::SIZE])
        if self.bingo:
            self.winning_number = number

    # As described in the puzzle, a card's score is the sum of the unmarked numbers,
    # multiplied by the last drawn number that created a bingo
    def score(self):
        return sum(n for (n,i) in self.numbers.items() if not self.marked[i]) * self.winning_number

# Read cards from the input
cards = [BingoCard(card) for card in raw[1:]]

# Play bingo. Returns the winner and the loser, solving both parts at once
def play(draw, cards):
    winner = None
    winner_count = 0
    card_count = len(cards)
    for number in draw:
        for card in cards:
            card.mark(number)

            if card.bingo:
                if winner_count == 0:
                    winner = card

                winner_count += 1
                if winner_count == card_count:
                    return (winner, card)

        cards = [card for card in cards if not card.bingo]

    return winner_count

winner, loser = play(draw, cards)

print("Part 1:")
print(winner.score())

print("Part 2:")
print(loser.score())
