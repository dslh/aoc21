#!/usr/bin/env python3

from get_aoc import get_input_chunks

raw = get_input_chunks(4)

# The numbers to be drawn from the barrel
draw = [int(n) for n in raw[0].split(',')]

SIZE = 5

# A class representing a bingo card. Stores the numbers on the card, keeps track of which
# ones have been marked, and detects bingo.
class BingoCard:
    # Create a new card from a chunk of text
    def __init__(self, text):
        # The numbers on the card. Stored as a flat list.
        self.numbers = [int(n) for n in text.split()]

        # Set up the list of which numbers have been marked
        self.reset()

        # Flag denoting if the card has achieved bingo
        self.bingo = False

    def reset(self):
        # A list of booleans corresponding to numbers, marking the positions that have been drawn
        self.marked = [False] * len(self.numbers)


    # Reproduce the original text used to generate the card
    def __str__(self):
        rows = [self.numbers[i:i+SIZE] for i in range(0, len(self.numbers), SIZE)]
        return '\n'.join(' '.join(str(n).rjust(2, ' ') for n in row) for row in rows)

    # Convert a positin in the list to row and column
    def _get_coords(self, position):
        return (position // SIZE, position % SIZE)

    def _is_row_bingo(self, row):
        offset = row * SIZE
        return all(mark for mark in self.marked[offset:offset+SIZE])

    def _is_col_bingo(self, col):
        return all(mark for mark in self.marked[col::SIZE])

    def mark(self, number):
        try:
            position = self.numbers.index(number)
        except ValueError:
            return

        self.marked[position] = True

        if self.bingo:
            return

        row, col = self._get_coords(position)
        self.bingo = self._is_row_bingo(row) or self._is_col_bingo(col)
        if self.bingo:
            self.winning_number = number

    def unmarked(self):
        return [self.numbers[i] for i in range(len(self.numbers)) if not self.marked[i]]

cards = [BingoCard(card) for card in raw[1:]]

contains_number = {i:[] for i in draw}
for card in cards:
    for number in card.numbers:
        contains_number[number].append(card)

def perform_draw(draw, cards_containing):
    for number in draw:
        for card in cards_containing[number]:
            card.mark(number)
            if card.bingo:
                return card

winner = perform_draw(draw, contains_number)

print("Part 1:")
print(sum(winner.unmarked()) * winner.winning_number)

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
print(sum(loser.unmarked()) * loser.winning_number)
