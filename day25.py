#!/usr/bin/env python3

def move_herd(herd, other, dir, limit):
    out = set()
    for cucumber in herd:
        new_pos = tuple((cucumber[i] + dir[i]) % limit[i] for i in range(2))
        if new_pos in herd or new_pos in other:
            out.add(cucumber)
        else:
            out.add(new_pos)

    return out

def move_all(east, south, limit):
    new_east = move_herd(east, south, (1,0), limit)
    new_south = move_herd(south, new_east, (0,1), limit)

    return (new_east, new_south)

from time import sleep
def show(east, south, limit):
    for y in range(limit[1]):
        for x in range(limit[0]):
            pos = (x, y)
            if pos in east:
                print('>', end='')
            elif pos in south:
                print('v', end='')
            else:
                print('.', end='')

        print()

def run(east, south, limit):
    step = 0
    while True:
        new_east, new_south = move_all(east, south, limit)
        step += 1

        if new_east == east and new_south == south:
            return (step, new_east, new_south)

        east = new_east
        south = new_south

def parse(lines):
    east = set()
    south = set()
    limit = (len(lines[0]), len(lines))
    for x in range(limit[0]):
        for y in range(limit[1]):
            c = lines[y][x]
            if c == '>':
                east.add((x, y))
            elif c == 'v':
                south.add((x, y))

    return east, south, limit


if __name__ == '__main__':
    from get_aoc import get_input_lines

    east, south, LIMIT = parse(get_input_lines(25))

    step, new_east, new_south = run(east, south, LIMIT)
    print('Part 1:')
    print(step)

