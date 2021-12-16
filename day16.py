#!/usr/bin/env python3

from queue import Queue, Empty
from math import prod

class BitReader:
    # input seems to be 8-bit aligned
    WIDTH = 8

    def __init__(self, encoded):
        # How many bits we've read so far
        self.position = 0

        # The data stored as a queue of bytes
        self.data = Queue()
        for i in range(0, len(encoded), 2):
            self.data.put(int(encoded[i:i+2], 16))

        # Load the first byte for reading
        self.next_byte()

    def next_byte(self):
        # current byte
        self.byte = self.data.get(False)
        # bits remaining to be read from the current byte
        self.offset = BitReader.WIDTH

    def read(self, bits):
        self.position += bits

        out = 0
        while bits >= self.offset:
            out <<= self.offset
            mask = (1 << self.offset) - 1
            out += self.byte & mask

            bits -= self.offset
            self.next_byte()

        out <<= bits
        self.offset -= bits
        mask = ((1 << bits) - 1) << self.offset
        out += (self.byte & mask) >> self.offset

        return out

    def read_literal(self):
        out = 0
        while True:
            group = self.read(5)
            out += group & 15

            if not group & 16:
                break

            out <<= 4

        return out

    def read_packet(self):
        version = self.read(3)
        pkt_type = self.read(3)

        if pkt_type == 4:
            return LiteralPacket(version, pkt_type, self.read_literal())

        return OperatorPacket(version, pkt_type, self.read_subpackets())

    def read_subpackets(self):
        if self.read(1):
            return self.read_packets(self.read(11))
        else:
            return self.read_bits(self.read(15))

    def read_packets(self, count):
        return [self.read_packet() for _ in range(count)]

    def read_bits(self, count):
        until_pos = self.position + count

        packets = []
        while self.position < until_pos:
            packets.append(self.read_packet())

        return packets

class LiteralPacket:
    def __init__(self, version, pkt_type, literal):
        self.version = version
        self.type = pkt_type
        self.literal = literal

    def version_sum(self):
        return self.version

    def value(self):
        return self.literal

def packet_sum(payload):
    return sum(packet.value() for packet in payload)

def packet_prod(payload):
    return prod(packet.value() for packet in payload)

def packet_min(payload):
    return min(packet.value() for packet in payload)

def packet_max(payload):
    return max(packet.value() for packet in payload)

def packet_gt(payload):
    return payload[0].value() > payload[1].value()

def packet_lt(payload):
    return payload[0].value() < payload[1].value()

def packet_eq(payload):
    return payload[0].value() == payload[1].value()

class OperatorPacket:
    OPERATORS = {
        0: packet_sum,
        1: packet_prod,
        2: packet_min,
        3: packet_max,
        5: packet_gt,
        6: packet_lt,
        7: packet_eq
    }

    def __init__(self, version, pkt_type, payload):
        self.version = version
        self.type = pkt_type
        self.payload = payload

    def version_sum(self):
        return self.version + sum(packet.version_sum() for packet in self.payload)

    def value(self):
        return OperatorPacket.OPERATORS[self.type](self.payload)

if __name__ == '__main__':
    from get_aoc import get_input

    reader = BitReader(get_input(16))
    packet = reader.read_packet()

    print('Part 1:')
    print(packet.version_sum())

    print('Part 2:')
    print(packet.value())
