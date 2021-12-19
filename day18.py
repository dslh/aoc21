#!/usr/bin/env python3

from itertools import permutations

LEFT = True
RIGHT = False

class Leaf:
    def __init__(self, number, parent, side):
        self.number = number
        self.parent = parent
        self.side = side

    def split(self):
        split = [self.number // 2] * 2
        split[1] += self.number % 2

        return self.parent.set(Tree(split, self.parent, self.side))

    def leftmost_leaf(self):
        return self

    def rightmost_leaf(self):
        return self

    def traverse_trees(self, depth):
        yield from ()

    def traverse_leaves(self, depth):
        yield (self, depth)

    def list(self):
        return self.number

    def magnitude(self):
        return self.number

class Tree:
    def __init__(self, number, parent=None, side=None):
        self.parent = parent
        self.side = side

        left, right = number
        self.left = self._read(left, LEFT)
        self.right = self._read(right, RIGHT)

    def _read(self, number, side):
        if type(number) == int:
            return Leaf(number, self, side)
        else:
            return Tree(number, self, side)

    def traverse_trees(self, depth=0):
        yield (self, depth)

        yield from self.left.traverse_trees(depth + 1)
        yield from self.right.traverse_trees(depth + 1)

    def traverse_leaves(self, depth=0):
        yield from self.left.traverse_leaves(depth + 1)
        yield from self.right.traverse_leaves(depth + 1)

    def set(self, child):
        if child.side == LEFT:
            self.left = child
        else:
            self.right = child

        return child

    def is_simple(self):
        return type(self.left) == Leaf and type(self.right) == Leaf

    def explode(self):
        left_leaf = self.left_adjacent_leaf()
        if left_leaf:
            left_leaf.number += self.left.number

        right_leaf = self.right_adjacent_leaf()
        if right_leaf:
            right_leaf.number += self.right.number

        self.parent.set(Leaf(0, self.parent, self.side))

    def left_adjacent_leaf(self):
        if not self.parent:
            return

        if self.side == LEFT:
            return self.parent.left_adjacent_leaf()
        else:
            return self.parent.left.rightmost_leaf()

    def right_adjacent_leaf(self):
        if not self.parent:
            return

        if self.side == RIGHT:
            return self.parent.right_adjacent_leaf()
        else: return self.parent.right.leftmost_leaf()

    def leftmost_leaf(self):
        return self.left.leftmost_leaf()

    def rightmost_leaf(self):
        return self.right.rightmost_leaf()

    def list(self):
        return [self.left.list(), self.right.list()]

    def reduce(self):
        reduced = True
        while reduced:
            reduced = False
            for node, depth in self.traverse_trees():
                if depth >= 4 and node.is_simple():
                    node.explode()
                    reduced = True
                    break

            if not reduced:
                for node, depth in self.traverse_leaves():
                    if node.number >= 10:
                        node.split()
                        reduced = True
                        break

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, other):
        result = Tree([self.list(), other.list()])
        result.reduce()
        return result

def max_magnitude(trees):
    return max((a + b).magnitude() for a, b in permutations(trees, 2))

if __name__ == '__main__':
    from get_aoc import get_input_lines
    numbers = [Tree(eval(line)) for line in get_input_lines(18)]

    number = sum(numbers[1:], numbers[0])
    print('Part 1:')
    print(number.magnitude())

    print('Part 2:')
    print(max_magnitude(numbers))
