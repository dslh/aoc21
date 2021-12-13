#!/usr/bin/env python3

def _parse_dot(dot):
    x, y = dot.split(',')
    return int(x), int(y)

def parse_fold(instruction):
    axis, position = instruction.strip('fold along').split('=')
    return axis, int(position)

def _folded(value, fold):
    if value <= fold:
        return value
    else:
        return fold * 2 - value

class Sheet:
    def __init__(self, dots):
        self.dots = {_parse_dot(dot) for dot in dots}

    def fold(self, axis, position):
        if axis == 'x':
            folder = lambda x, y: (_folded(x, position), y)
        else:
            folder = lambda x, y: (x, _folded(y, position))

        self.dots = {folder(*dot) for dot in self.dots}

    def __str__(self):
        WIDTH = max(x for x,_ in self.dots) + 1
        HEIGHT = max(y for _,y in self.dots) + 1
        return "\n".join(
            "".join(
                self._chr(x, y) for x in range(WIDTH)
            ) for y in range(HEIGHT)
        )

    def _chr(self, x, y):
        return '#' if (x, y) in self.dots else '.'

if __name__ == '__main__':
    from get_aoc import get_input_chunks

    dots, folds = [chunk.split('\n') for chunk in get_input_chunks(13)]
    folds = [parse_fold(fold) for fold in folds]

    sheet = Sheet(dots)
    sheet.fold(*folds[0])
    print("Part 1")
    print(len(sheet.dots))

    for fold in folds[1:]:
        sheet.fold(*fold)

    print("Part 2")
    print(sheet)
