#!/usr/bin/env python3

import re
from queue import PriorityQueue

ITEM_MASK = 0b11

# One of the four rooms where the crabs live.
# Immutable; rather than modifying the room we return copies of the room
# in a new state, so that we can re-use a room object across multiple positions
# during the search without running into problems.
class Room:
    def __init__(self, category, size, contents, amount):
        # The type of crab that lives in this room
        self.category = category
        # The number of crabs that can fit here
        self.size = size
        # The crabs currently inhabiting the room, packed into an integer
        self.contents = contents
        # The number of crabs currently inhabiting the room
        self.amount = amount

        # The base cost for moving from the door to the first unoccupied spot.
        # Add one to this cost when you're leaving the room.
        self.cost = size - amount

        # True when all the crabs that don't live here are cleared out
        self.filling = all(item == category for item in self.items())
        # True when there are still some crabs that need to leave
        self.emptying = not self.filling
        # True when all the crabs that live here are home
        self.filled = self.filling and amount == size

    # Position of a room, for calculating distances and costs
    @staticmethod
    def pos(category):
        return (category + 1) * 2

    # For initializing the room from the problem input.
    @classmethod
    def new(cls, category, items):
        contents = 0
        for item in reversed(items):
            contents = (contents << 2) | (ord(item) - ord('A'))

        return cls(category, len(items), contents, len(items))

    # Enumerates the crabs in the room, starting with the crab closest to the door.
    def items(self):
        for i in range(self.amount):
            yield (self.contents >> (i * 2)) & ITEM_MASK

    # Returns the category of the crab closest to the door.
    def peek(self):
        return self.contents & ITEM_MASK

    # Shove a new crab into the room.
    def push(self, item):
        return Room(self.category, self.size, self.contents << 2 | item, self.amount + 1)

    # Yank the crab closest to the door out of the room.
    def pop(self):
        return Room(self.category, self.size, self.contents >> 2, self.amount - 1)

# The hallway connecting the rooms.
# Hard-coded to assume four rooms, with two free spaces on either side of the rooms,
# and one free space in between each room.
# Rooms are therefore between hallway positions 1 and 2, 2 and 3, 3 and 4, and 4 and 5,
# given that there are 7 positions numbered 0-6.
# Immutable, like Room.
class Hallway:
    def __init__(self, contents = 0, filled = 0):
        # Like with Room, crabs get packed into a single integer.
        self.contents = contents
        # Bit flags denoting which positions have a crab in them.
        self.filled = filled

    # Position of a hall slot, for calculating distances and costs.
    @staticmethod
    def pos(i):
        if i < 2:
            return i

        if i == 6:
            return 10

        return (i - 1) * 2 + 1

    # Return the type of crab present at position i.
    def __getitem__(self, i):
        if not self.filled & 1 << i:
            return None

        return self.contents >> i * 2 & ITEM_MASK

    # List all of the positions where there is a crab, along with the crab's type.
    def items(self):
        for i in range(7):
            item = self[i]
            if item != None:
                yield (i, item)

    # Put a crab at position i.
    def put(self, i, item):
        if self.filled & 1 << i:
            raise IndexError

        contents = self.contents | item << (i * 2)
        filled = self.filled | 1 << i

        return Hallway(contents, filled)

    # Remove the crab at position i.
    def take(self, i):
        if not self.filled & 1 << i:
            raise IndexError

        contents = self.contents & ~(ITEM_MASK << (i * 2))
        filled = self.filled & ~(1 << i)

        return Hallway(contents, filled)

    # Hall positions that can be reached from a room.
    def room_to_hall(self, source_room):
        for i in range(source_room + 1, -1, -1):
            if self.filled & 1 << i:
                break

            yield i

        for i in range(source_room + 2, 7):
            if self.filled & 1 << i:
                break

            yield i

    # True if a room can be reached from a hall position.
    def hall_to_room(self, i, room):
        room += 2
        if i > room:
            r = range(room, i)
        else:
            r = range(i + 1, room)

        return all(not self.filled & 1 << i for i in r)

    # True if a room can be reached from another room.
    def room_to_room(self, source, dest):
        a = min(source, dest)
        b = max(source, dest)

        return all(not self.filled & 1 << i for i in range(a + 2, b + 2))

class Burrow:
    def __init__(self, rooms, hall=Hallway(), cost=0, prev=None):
        self.rooms = rooms
        self.hall = hall
        self.cost = cost
        self.prev = prev

        self.done = all(room.filled for room in rooms)

    @classmethod
    def parse(cls, input, part_twoify=False):
        cols = list(zip(*(
            re.findall(r'[A-D]', line) for line in input.split('\n')[2:-1]
        )))

        if part_twoify:
            cols[0] = [cols[0][0], 'D', 'D', cols[0][1]]
            cols[1] = [cols[1][0], 'C', 'B', cols[1][1]]
            cols[2] = [cols[2][0], 'B', 'A', cols[2][1]]
            cols[3] = [cols[3][0], 'A', 'C', cols[3][1]]

        rooms = [Room.new(i, col) for i, col in enumerate(cols)]

        return cls(rooms)

    # Order burrows by their cost. Needed for PriorityQueue.
    def __lt__(self, other):
        return self.cost < other.cost

    # All of the valid moves that can be made from this position.
    def moves(self):
        for i, room in enumerate(self.rooms):
            if not room.emptying:
                continue

            item = room.peek()
            if self.rooms[item].filling and self.hall.room_to_room(i, item):
                yield self.room_to_room(i, item)
            else:
                for j in self.hall.room_to_hall(i):
                    yield self.room_to_hall(i, j)

        for i, item in self.hall.items():
            if self.rooms[item].filling and self.hall.hall_to_room(i, item):
                yield self.hall_to_room(i, item)

    # Return a new Burrow object where the crab closest to the door in the source room
    # has moved all the way to the destination room. Assumes that crabs always move to
    # the room where they belong (i.e. dest == crab category).
    def room_to_room(self, source, dest):
        cost = (
            abs(Room.pos(source) - Room.pos(dest)) +
            self.rooms[source].cost + 1 +
            self.rooms[dest].cost
        )
        cost *= 10 ** dest

        rooms = self.rooms.copy()
        rooms[source] = rooms[source].pop()
        rooms[dest] = rooms[dest].push(dest)

        return Burrow(rooms, self.hall, self.cost + cost, self)

    def room_to_hall(self, room, i):
        item = self.rooms[room].peek()

        cost = abs(Room.pos(room) - Hallway.pos(i)) + self.rooms[room].cost + 1
        cost *= 10 ** item

        rooms = self.rooms.copy()
        rooms[room] = rooms[room].pop()

        hall = self.hall.put(i, item)

        return Burrow(rooms, hall, self.cost + cost, self)

    def hall_to_room(self, i, room):
        cost = abs(Room.pos(room) - Hallway.pos(i)) + self.rooms[room].cost
        cost *= 10 ** room

        rooms = self.rooms.copy()
        rooms[room] = rooms[room].push(room)

        hall = self.hall.take(i)

        return Burrow(rooms, hall, self.cost + cost, self)

def search(burrow):
    moves = PriorityQueue()

    while not burrow.done:
        for move in burrow.moves():
            moves.put(move)

        burrow = moves.get_nowait()

    return burrow

if __name__ == '__main__':
    from get_aoc import get_input

    burrow = Burrow.parse(get_input(23))
    print("Part 1:")
    print(search(burrow).cost)

    burrow = Burrow.parse(get_input(23), True)
    print("Part 2:")
    print(search(burrow).cost)
