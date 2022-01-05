import pytest
import context

from day23 import Room, Hallway, Burrow, search

def test_room():
    room = Room.new(3, ['A','B','C','D'])
    assert room.category == 3
    assert room.emptying
    assert not room.filling
    assert not room.filled
    assert room.size == 4
    assert room.amount == 4
    assert list(room.items()) == [0,1,2,3]
    assert room.peek() == 0
    assert room.cost == 0

    room = room.pop()
    assert room.category == 3
    assert room.emptying
    assert not room.filling
    assert not room.filled
    assert room.size == 4
    assert room.amount == 3
    assert list(room.items()) == [1,2,3]
    assert room.peek() == 1
    assert room.cost == 1

    room = room.pop().pop()
    assert not room.emptying
    assert room.filling
    assert not room.filled
    assert room.amount == 1
    assert list(room.items()) == [3]
    assert room.peek() == 3
    assert room.cost == 3

    assert room.pop().filling

    room = room.push(3).push(3).push(3)
    assert not room.emptying
    assert room.filled
    assert room.amount == 4
    assert list(room.items()) == [3,3,3,3]
    assert room.cost == 0

    assert list(Room.pos(i) for i in range(4)) == [2,4,6,8]

def test_hallway():
    hall = Hallway()
    assert len(list(hall.items())) == 0
    for room in range(4):
        assert sorted(list(hall.room_to_hall(room))) == [0,1,2,3,4,5,6]
        for other in range(4):
            if other != room:
                assert hall.room_to_room(room, other)
                assert hall.room_to_room(other, room)

        for i in range(7):
            assert hall.hall_to_room(i, room)

    hall = hall.put(3, 2)
    assert hall[3] == 2
    assert list(hall.items()) == [(3, 2)]
    assert sorted(hall.room_to_hall(0)) == [0,1,2]
    assert sorted(hall.room_to_hall(1)) == [0,1,2]
    assert sorted(hall.room_to_hall(2)) == [4,5,6]
    assert sorted(hall.room_to_hall(3)) == [4,5,6]
    assert hall.room_to_room(0,1)
    assert hall.room_to_room(2,3)
    assert not hall.room_to_room(1,2)
    assert not hall.room_to_room(3,0)
    for i in range(3):
        assert hall.hall_to_room(i,0)
        assert hall.hall_to_room(i,1)
        assert not hall.hall_to_room(i,2)
        assert not hall.hall_to_room(i,3)
    for i in range(4,7):
        assert not hall.hall_to_room(i,0)
        assert not hall.hall_to_room(i,1)
        assert hall.hall_to_room(i,2)
        assert hall.hall_to_room(i,3)

    hall = hall.take(3)
    assert len(list(hall.items())) == 0

    for i in range(7):
        hall = hall.put(i, i % 4)

    assert list(hall.items()) == [(0,0),(1,1),(2,2),(3,3),(4,0),(5,1),(6,2)]
    for room in range(4):
        assert len(list(hall.room_to_hall(room))) == 0
        for other in range(4):
            if room != other:
                assert not hall.room_to_room(room, other)
                assert not hall.room_to_room(other, room)
        for i in range(7):
            if 0 <= (i - room - 1) <= 1:
                assert hall.hall_to_room(i, room)
            else:
                assert not hall.hall_to_room(i, room)

    assert list(Hallway.pos(i) for i in range(7)) == [0,1,3,5,7,9,10]

from inspect import cleandoc

@pytest.fixture
def sample_input():
    return cleandoc("""
        #############
        #...........#
        ###B#C#B#D###
          #A#D#C#A#
          #########""")

@pytest.fixture
def extended_sample_input():
    return cleandoc("""
        #############
        #...........#
        ###B#C#B#D###
          #D#C#B#A#
          #D#B#A#C#
          #A#D#C#A#
          #########""")

def test_burrow_parse(sample_input, extended_sample_input):
    burrow = Burrow.parse(sample_input)
    assert list(burrow.rooms[0].items()) == [1,0]
    assert list(burrow.rooms[1].items()) == [2,3]
    assert list(burrow.rooms[2].items()) == [1,2]
    assert list(burrow.rooms[3].items()) == [3,0]
    for i, room in enumerate(burrow.rooms):
        assert room.category == i
        assert room.size == 2
        assert room.emptying
    assert len(list(burrow.hall.items())) == 0
    assert burrow.cost == 0

    burrow = Burrow.parse(extended_sample_input)
    assert list(burrow.rooms[0].items()) == [1,3,3,0]
    assert list(burrow.rooms[1].items()) == [2,2,1,3]
    assert list(burrow.rooms[2].items()) == [1,1,0,2]
    assert list(burrow.rooms[3].items()) == [3,0,2,0]
    for i, room in enumerate(burrow.rooms):
        assert room.category == i
        assert room.size == 4
        assert room.emptying

def test_burrow_moves(sample_input):
    burrow = Burrow.parse(sample_input)
    assert len(list(burrow.moves())) == 4 * 7

    burrow = burrow.room_to_hall(2, 2)
    assert burrow.cost == 40
    assert list(burrow.hall.items()) == [(2,1)]
    assert list(burrow.rooms[2].items()) == [2]
    assert burrow.rooms[2].filling

    burrow = burrow.room_to_room(1, 2)
    assert burrow.cost == 440
    assert list(burrow.rooms[2].items()) == [2,2]
    assert list(burrow.rooms[1].items()) == [3]
    assert burrow.rooms[2].filled

    burrow = burrow.room_to_hall(1,3)
    assert burrow.cost == 3440
    assert list(burrow.hall.items()) == [(2,1),(3,3)]
    burrow = burrow.hall_to_room(2,1)
    assert burrow.cost == 3470

    burrow = burrow.room_to_room(0,1)
    assert burrow.cost == 3510
    assert burrow.rooms[1].filled
    assert list(burrow.rooms[0].items()) == [0]

    burrow = burrow.room_to_hall(3,4)
    assert burrow.cost == 5510
    assert list(burrow.hall.items()) == [(3,3),(4,3)]

    burrow = burrow.room_to_hall(3,5)
    assert burrow.cost == 5513
    assert list(burrow.hall.items()) == [(3,3),(4,3),(5,0)]
    assert burrow.rooms[3].filling
    assert not burrow.rooms[3].emptying

    burrow = burrow.hall_to_room(4,3)
    burrow = burrow.hall_to_room(3,3)
    assert burrow.cost == 12513
    assert burrow.rooms[3].filled
    assert not burrow.done

    burrow = burrow.hall_to_room(5,0)
    assert burrow.cost == 12521
    assert burrow.done

def test_search(sample_input, extended_sample_input):
    burrow = Burrow.parse(sample_input)
    burrow = search(burrow)
    assert burrow.done
    assert burrow.cost == 12521
