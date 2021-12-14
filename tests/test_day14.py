import pytest

import context

from day14 import Polymizer, pairwise, polymer_rating

@pytest.fixture
def sample_rules():
    return [
        'CH -> B',
        'HH -> N',
        'CB -> H',
        'NH -> C',
        'HB -> C',
        'HC -> B',
        'HN -> C',
        'NN -> C',
        'BH -> H',
        'NC -> B',
        'NB -> B',
        'BN -> B',
        'BB -> N',
        'BC -> B',
        'CC -> N',
        'CN -> C'
    ]

@pytest.fixture
def sample_expansion():
    return [
        'NNCB',
        'NCNBCHB',
        'NBCCNBBBCBHCB',
        'NBBBCNCCNBBNBNBBCHBHHBCHB',
        'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    ]

def test_pairwise():
    assert list(pairwise([1, 2, 3, 4])) == [[1,2], [2,3], [3,4]]
    assert list(pairwise("abcd")) == ["ab", "bc", "cd"]

def test_init():
    polymizer = Polymizer(['CH -> B', 'HH -> N'])

    assert polymizer.rules == {
        'CH': 'CB',
        'HH': 'HN'
    }

def test_expand(sample_rules, sample_expansion):
    polymizer = Polymizer(sample_rules)

    for base, expanded in pairwise(sample_expansion):
        assert polymizer.expand(base) == expanded

    template = sample_expansion[0]

    assert polymizer.expand_n(template, 4) == sample_expansion[-1]
    assert len(polymizer.expand_n(template, 5)) == 97

    tenth = polymizer.expand_n(template, 10)
    assert len(tenth) == 3073
    assert tenth.count('B') == 1749
    assert tenth.count('C') == 298
    assert tenth.count('H') == 161
    assert tenth.count('N') == 865

def test_polymer_rating(sample_rules):
    assert polymer_rating('NNCB') == 1

    polymizer = Polymizer(sample_rules)
    expanded = polymizer.expand_n('NNCB', 10)
    assert polymer_rating(expanded) == 1588
