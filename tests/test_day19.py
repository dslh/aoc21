import pytest
import context

from day19 import Field, overlay_all

from os.path import dirname, join

@pytest.fixture
def sample_chunks():
    filename = join(dirname(__file__), 'fixtures/19.txt')
    return open(filename, 'r').read().strip().split('\n\n')

@pytest.fixture
def sample_orientations():
    filename = join(dirname(__file__), 'fixtures/19.orientations.txt')
    return open(filename, 'r').read().strip().split('\n\n')

# Testing a theory.
def test_distances(sample_chunks):
    a = Field(sample_chunks[0])
    b = Field(sample_chunks[1])
    e = Field(sample_chunks[4])
    assert len(a.distances & b.distances) == 66
    assert len(b.distances & e.distances) == 66

def test_orientations(sample_orientations):
    fields = [Field(chunk) for chunk in sample_orientations]
    field = fields[0]
    orientations = fields[1:]

    matches = 0
    for orientation in field.orientations():
        for sample in orientations:
            if set(orientation) == set(sample.coords):
                matches += 1

    assert matches == len(orientations)

def test_overlay(sample_chunks):
    a = Field(sample_chunks[0])
    b = Field(sample_chunks[1])
    e = Field(sample_chunks[4])

    assert b.overlay(a)
    assert b.centre == (68,-1246,-43)

    coords = set(b.coords)
    assert (-618,-824,-621) in coords
    assert (-537,-823,-458) in coords
    assert (-447,-329,318) in coords
    assert (404,-588,-901) in coords
    assert (544,-627,-890) in coords
    assert (528,-643,409) in coords
    assert (-661,-816,-575) in coords
    assert (390,-675,-793) in coords
    assert (423,-701,434) in coords
    assert (-345,-311,381) in coords
    assert (459,-707,401) in coords
    assert (-485,-357,347) in coords

    assert e.overlay(b)
    assert e.centre == (-20,-1133,1061)

    coords = set(e.coords)
    assert (459,-707,401) in coords
    assert (-739,-1745,668) in coords
    assert (-485,-357,347) in coords
    assert (432,-2009,850) in coords
    assert (528,-643,409) in coords
    assert (423,-701,434) in coords
    assert (-345,-311,381) in coords
    assert (408,-1815,803) in coords
    assert (534,-1912,768) in coords
    assert (-687,-1600,576) in coords
    assert (-447,-329,318) in coords
    assert (-635,-1737,486) in coords

def test_overlay_all(sample_chunks):
    fields = [Field(chunk) for chunk in sample_chunks]

    overlay_all(fields)
    assert fields[1].centre == (68,-1246,-43)
    assert fields[2].centre == (1105,-1205,1229)
    assert fields[3].centre == (-92,-2380,-20)
    assert fields[4].centre == (-20,-1133,1061)

    coords = set(coord for field in fields for coord in field.coords)
    assert len(coords) == 79
    assert (-892,524,684) in coords
    assert (-876,649,763) in coords
    assert (-838,591,734) in coords
    assert (-789,900,-551) in coords
    assert (-739,-1745,668) in coords
    assert (-706,-3180,-659) in coords
    assert (-697,-3072,-689) in coords
    assert (-689,845,-530) in coords
    assert (-687,-1600,576) in coords
    assert (-661,-816,-575) in coords
    assert (-654,-3158,-753) in coords
    assert (-635,-1737,486) in coords
    assert (-631,-672,1502) in coords
    assert (-624,-1620,1868) in coords
    assert (-620,-3212,371) in coords
    assert (-618,-824,-621) in coords
    assert (-612,-1695,1788) in coords
    assert (-601,-1648,-643) in coords
    assert (-584,868,-557) in coords
    assert (-537,-823,-458) in coords
    assert (-532,-1715,1894) in coords
    assert (-518,-1681,-600) in coords
    assert (-499,-1607,-770) in coords
    assert (-485,-357,347) in coords
    assert (-470,-3283,303) in coords
    assert (-456,-621,1527) in coords
    assert (-447,-329,318) in coords
    assert (-430,-3130,366) in coords
    assert (-413,-627,1469) in coords
    assert (-345,-311,381) in coords
    assert (-36,-1284,1171) in coords
    assert (-27,-1108,-65) in coords
    assert (7,-33,-71) in coords
    assert (12,-2351,-103) in coords
    assert (26,-1119,1091) in coords
    assert (346,-2985,342) in coords
    assert (366,-3059,397) in coords
    assert (377,-2827,367) in coords
    assert (390,-675,-793) in coords
    assert (396,-1931,-563) in coords
    assert (404,-588,-901) in coords
    assert (408,-1815,803) in coords
    assert (423,-701,434) in coords
    assert (432,-2009,850) in coords
    assert (443,580,662) in coords
    assert (455,729,728) in coords
    assert (456,-540,1869) in coords
    assert (459,-707,401) in coords
    assert (465,-695,1988) in coords
    assert (474,580,667) in coords
    assert (496,-1584,1900) in coords
    assert (497,-1838,-617) in coords
    assert (527,-524,1933) in coords
    assert (528,-643,409) in coords
    assert (534,-1912,768) in coords
    assert (544,-627,-890) in coords
    assert (553,345,-567) in coords
    assert (564,392,-477) in coords
    assert (568,-2007,-577) in coords
    assert (605,-1665,1952) in coords
    assert (612,-1593,1893) in coords
    assert (630,319,-379) in coords
    assert (686,-3108,-505) in coords
    assert (776,-3184,-501) in coords
    assert (846,-3110,-434) in coords
    assert (1135,-1161,1235) in coords
    assert (1243,-1093,1063) in coords
    assert (1660,-552,429) in coords
    assert (1693,-557,386) in coords
    assert (1735,-437,1738) in coords
    assert (1749,-1800,1813) in coords
    assert (1772,-405,1572) in coords
    assert (1776,-675,371) in coords
    assert (1779,-442,1789) in coords
    assert (1780,-1548,337) in coords
    assert (1786,-1538,337) in coords
    assert (1847,-1591,415) in coords
    assert (1889,-1729,1762) in coords
    assert (1994,-1805,1792) in coords
