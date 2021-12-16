import pytest

import context
from day16 import BitReader

# v6 literal 2021
@pytest.fixture
def pkt_one():
    return 'D2FE28'

# v1 type 6
#  - literal 10
#  - literal 20
@pytest.fixture
def pkt_two():
    return '38006F45291200'

# v7 type 3
#  - literal 1
#  - literal 2
#  - literal 3
@pytest.fixture
def pkt_three():
    return 'EE00D40C823060'

# v4 operator
#  - v1 operator
#    - v5 operator
#      - v6 literal
# version sum 16
@pytest.fixture
def pkt_four():
    return '8A004A801A8002F478'

# v3 operator
#  - 2 * operator, each containing
#    - 2 * literal
# version sum 12
@pytest.fixture
def pkt_five():
    return '620080001611562C8802118E34'

# operator
#  - 2 * operator, each containing
#    - 2 * literal
# version sum 23
@pytest.fixture
def pkt_six():
    return 'C0015000016115A2E0802F182340'

# operator
#  - operator
#    - 5 * literal
# version sum 31
@pytest.fixture
def pkt_seven():
    return 'A0016C880162017C3686B18A3D4780'

def test_read_bytes(pkt_one, pkt_two):
    reader = BitReader(pkt_one)
    assert reader.read(3) == 6
    assert reader.read(3) == 4
    assert reader.read(5) == 0b10111
    assert reader.read(5) == 0b11110
    assert reader.read(5) == 0b00101

    reader = BitReader(pkt_two)
    assert reader.read(3) == 1
    assert reader.read(3) == 6
    assert reader.read(1) == 0
    assert reader.read(15) == 27

    # First subpacket
    reader.read(3) # version not specified
    assert reader.read(3) == 4
    assert reader.read(5) == 10

    # Second subpacket
    reader.read(3) # version not specified
    assert reader.read(3) == 4
    assert reader.read(5) == 0b10001
    assert reader.read(5) == 0b00100

def test_position(pkt_one):
    reader = BitReader(pkt_one)
    assert reader.position == 0
    reader.read(3)
    assert reader.position == 3
    reader.read(3)
    assert reader.position == 6
    reader.read_literal()
    assert reader.position == 21

def test_read_literal(pkt_one, pkt_two):
    reader = BitReader(pkt_one)
    reader.read(6) # skip the header
    assert reader.read_literal() == 2021

    reader = BitReader(pkt_two)
    reader.read(28) # skip to first subpacket payload
    assert reader.read_literal() == 10

    reader.read(6) # skip second subpacket header
    assert reader.read_literal() == 20

def test_read_packet_literal(pkt_one):
    reader = BitReader(pkt_one)
    packet = reader.read_packet()

    assert packet.version == 6
    assert packet.type == 4
    assert packet.literal == 2021

    assert packet.version_sum() == 6

def test_read_packet_operator(pkt_two, pkt_three):
    reader = BitReader(pkt_two)
    packet = reader.read_packet()

    assert packet.version == 1
    assert packet.type == 6
    assert len(packet.payload) == 2
    assert packet.payload[0].literal == 10
    assert packet.payload[1].literal == 20

    reader = BitReader(pkt_three)
    packet = reader.read_packet()
    assert packet.version == 7
    assert packet.type == 3
    assert len(packet.payload) == 3
    assert packet.payload[0].literal == 1
    assert packet.payload[1].literal == 2
    assert packet.payload[2].literal == 3

def test_nesting(pkt_four, pkt_five):
    reader = BitReader(pkt_four)
    four = reader.read_packet()

    assert four.version == 4
    assert len(four.payload) == 1
    assert four.payload[0].version == 1
    assert len(four.payload[0].payload) == 1
    assert four.payload[0].payload[0].version == 5
    assert len(four.payload[0].payload[0].payload) == 1
    assert four.payload[0].payload[0].payload[0].version == 6
    assert four.version_sum() == 16

    reader = BitReader(pkt_five)
    five = reader.read_packet()

    assert five.version == 3
    assert len(five.payload) == 2
    for packet in five.payload:
        assert len(packet.payload) == 2
        for literal in packet.payload:
            assert literal.literal > 0
    assert five.version_sum() == 12

def test_version_sum(pkt_six, pkt_seven):
    reader = BitReader(pkt_six)
    packet = reader.read_packet()
    assert packet.version_sum() == 23

    reader = BitReader(pkt_seven)
    packet = reader.read_packet()
    assert packet.version_sum() == 31

def test_value():
    reader = BitReader('C200B40A8200')
    assert reader.read_packet().value() == 3

    reader = BitReader('04005AC33890')
    assert reader.read_packet().value() == 54

    reader = BitReader('880086C3E88112')
    assert reader.read_packet().value() == 7

    reader = BitReader('CE00C43D881120')
    assert reader.read_packet().value() == 9

    reader = BitReader('D8005AC2A8F0')
    assert reader.read_packet().value() == 1

    reader = BitReader('F600BC2D8F00')
    assert reader.read_packet().value() == 0

    reader = BitReader('9C005AC2F8F0')
    assert reader.read_packet().value() == 0

    reader = BitReader('9C0141080250320F1802104A08')
    assert reader.read_packet().value() == 1
