#!/usr/bin/env python3

from collections import defaultdict
import re

SMALL = re.compile(r'^[a-z]+$')

class Caves:
    def __init__(self, links):
        self.links = defaultdict(lambda: set())
        for link in links:
            a, b = link.split('-')
            self.links[a].add(b)
            self.links[b].add(a)

    def all_paths(self, revisit=False):
        return self._search('start', [], set(), [], revisit, False)

    # Search through the caves for the 'end'
    # from the current `node`
    # having taken the current `path`
    # having `visited` a set of small caves
    # having already found a list of `paths`
    # allowing the `revisit` of a single small cave (part 2)
    # having already `revisited` said cave, or not
    def _search(self, node, path, visited, paths, revisit, revisited):
        if node == 'end':
            paths.append(path + ['end'])
            return

        revisiting = False
        if node in visited:
            if not revisit or revisited or node == 'start':
                return

            revisited = True
            revisiting = True

        small = SMALL.match(node)
        if small:
            visited.add(node)

        path.append(node)
        for neighbour in self.links[node]:
            self._search(neighbour, path, visited, paths, revisit, revisited)
        path.pop()

        if small and not revisiting:
            visited.remove(node)

        return paths

if __name__ == '__main__':
    from get_aoc import get_input_lines

    caves = Caves(get_input_lines(12))
    print("Part 1:")
    print(len(caves.all_paths()))

    print("Part 2:")
    print(len(caves.all_paths(revisit=True)))
