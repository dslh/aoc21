import pytest

import context
from day18 import Tree, max_magnitude

def test_init():
    number = [1,2]
    assert Tree(number).list() == number

    number = [[1,2],3]
    assert Tree(number).list() == number

    number = [9,[8,7]]
    assert Tree(number).list() == number

    number = [[1,9],[8,5]]
    assert Tree(number).list() == number

    number = [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
    assert Tree(number).list() == number

    number = [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
    assert Tree(number).list() == number

    number = [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
    assert Tree(number).list() == number

def test_traverse_leaves():
    tree = Tree([1,[2,3]])
    assert list((node.number, depth) for node, depth in tree.traverse_leaves()) == [
        (1, 1), (2, 2), (3, 2)
    ]

    tree = Tree([1,[2,[3,[4,[5,5]]]]])
    assert list((node.number, depth) for node, depth in tree.traverse_leaves()) == [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (5, 5)
    ]

    tree = Tree([[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]])
    assert list(node.number for node, _ in tree.traverse_leaves()) == [
        9, 3, 8, 0, 9, 6, 3, 7, 4, 9, 3
    ]
    assert list(depth for _, depth in tree.traverse_leaves()) == [
        3, 4, 4, 4, 4, 3, 4, 4, 4, 4, 2
    ]

    tree = Tree([[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]])
    assert list(node.number for node, _ in tree.traverse_leaves()) == [
        1, 3, 5, 3, 1, 3, 8, 7, 4, 9, 6, 9, 8, 2, 7, 3
    ]
    assert list(depth for _, depth in tree.traverse_leaves()) == [
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
    ]

def test_traverse_trees():
    tree = Tree([1, [2, 3]])
    assert list(subtree.list() for subtree, _ in tree.traverse_trees()) == [
        [1, [2, 3]],
        [2, 3]
    ]
    assert list(depth for _, depth in tree.traverse_trees()) == [0, 1]

    tree = Tree([[1,9],[8,5]])
    assert list(subtree.list() for subtree, _ in tree.traverse_trees()) == [
        [[1, 9], [8, 5]],
        [1, 9],
        [8, 5]
    ]
    assert list(depth for _, depth in tree.traverse_trees()) == [0, 1, 1]

    tree = Tree([[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]])
    assert list(subtree.list() for subtree, _ in tree.traverse_trees()) == [
        [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]],
        [[9,[3,8]],[[0,9],6]],
        [9,[3,8]],
        [3,8],
        [[0,9],6],
        [0,9],
        [[[3,7],[4,9]],3],
        [[3,7],[4,9]],
        [3,7],
        [4,9]
    ]
    assert list(depth for _, depth in tree.traverse_trees()) == [
        0, 1, 2, 3, 2, 3, 1, 2, 3, 3
    ]

def test_reduce_exploding():
    tree = Tree([[[[[9,8],1],2],3],4])
    tree.reduce()
    assert tree.list() == [[[[0,9],2],3],4]

    tree = Tree([7,[6,[5,[4,[3,2]]]]])
    tree.reduce()
    assert tree.list() == [7,[6,[5,[7,0]]]]

    tree = Tree([[6,[5,[4,[3,2]]]],1])
    tree.reduce()
    assert tree.list() == [[6,[5,[7,0]]],3]

    tree = Tree([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    tree.reduce()
    assert tree.list() == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

def test_reduce_splitting():
    tree = Tree([12,13])
    tree.reduce()
    assert tree.list() == [[6,6],[6,7]]

def test_addition():
    tree = Tree([[[[4,3],4],4],[7,[[8,4],9]]]) + Tree([1,1])
    assert tree.list() == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

    tree = Tree([1,1]) + Tree([2,2]) + Tree([3,3]) + Tree([4,4])
    assert tree.list() == [[[[1,1],[2,2]],[3,3]],[4,4]]

    tree += Tree([5,5])
    assert tree.list() == [[[[3,0],[5,3]],[4,4]],[5,5]]

    tree += Tree([6,6])
    assert tree.list() == [[[[5,0],[7,4]],[5,5]],[6,6]]

    tree = Tree([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]])
    tree += Tree([7,[[[3,7],[4,3]],[[6,3],[8,8]]]])
    assert tree.list() == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

    tree += Tree([[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]])
    assert tree.list() == [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

    tree += Tree([[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]])
    assert tree.list() == [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

    tree += Tree([7,[5,[[3,8],[1,4]]]])
    # [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[7, 8], [0, 8]], [[8, 9], [9, 0]]]] <- Mine
    # [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]] <- Expected
    assert tree.list() == [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

    tree += Tree([[2,[2,2]],[8,[8,1]]])
    assert tree.list() == [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

    tree += Tree([2,9])
    assert tree.list() == [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

    tree += Tree([1,[[[9,3],9],[[9,0],[0,7]]]])
    assert tree.list() == [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

    tree += Tree([[[5,[7,4]],7],1])
    assert tree.list() == [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

    tree += Tree([[[[4,2],2],6],[8,7]])
    assert tree.list() == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

def test_magnitude():
    assert Tree([9,1]).magnitude() == 29
    assert Tree([1,9]).magnitude() == 21
    assert Tree([[9,1],[1,9]]).magnitude() == 129

    assert Tree([[1,2],[[3,4],5]]).magnitude() == 143
    assert Tree([[[[0,7],4],[[7,8],[6,0]]],[8,1]]).magnitude() == 1384
    assert Tree([[[[1,1],[2,2]],[3,3]],[4,4]]).magnitude() == 445
    assert Tree([[[[3,0],[5,3]],[4,4]],[5,5]]).magnitude() == 791
    assert Tree([[[[5,0],[7,4]],[5,5]],[6,6]]).magnitude() == 1137
    assert Tree([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).magnitude() == 3488

@pytest.fixture
def homework_assignment():
    assignment = [
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
        [[[5,[2,8]],4],[5,[[9,9],0]]],
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
        [[[[5,4],[7,7]],8],[[8,3],8]],
        [[9,3],[[9,9],[6,[4,9]]]],
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    ]

    return [Tree(line) for line in assignment]

def test_part_one(homework_assignment):
    result = sum(homework_assignment[1:], homework_assignment[0])

    assert result.list() == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
    assert result.magnitude() == 4140

def test_part_two(homework_assignment):
    assert max_magnitude(homework_assignment) == 3993
