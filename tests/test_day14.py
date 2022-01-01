import pytest

import context

from day14 import Polymizer, PolymerCounter, pairwise, polymer_rating, pair_counts, pairwise_rating

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

@pytest.fixture
def sample_pair_counts():
    return {
        'NB': 2, 'BC': 2, 'CC': 1, 'CN': 1, 'BB': 2, 'CB': 2, 'BH': 1, 'HC': 1
    }

def test_pair_counts(sample_pair_counts):
    polymer = 'NBCCNBBBCBHCB'
    assert pair_counts(polymer) == sample_pair_counts

def test_polymer_counter(sample_rules, sample_pair_counts):
    polymer = 'NNCB'
    counter = PolymerCounter(sample_rules, polymer)
    counter.expand_n(10)

    counts = counter.counts()
    assert counts['B'] == 1749
    assert counts['C'] == 298
    assert counts['H'] == 161
    assert counts['N'] == 865

    assert counter.rating() == 1588

    counter.expand_n(30)
    counts = counter.counts()
    assert counts['B'] == 2192039569602
    assert counts['H'] == 3849876073
    assert counter.rating() == 2188189693529
