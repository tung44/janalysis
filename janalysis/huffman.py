"""Defines functions to make huffman coding of values (not really specific
to JPEG at all (certain specifics about JPEG are currently ignored such as
the rule about 1's and the rule about code length).
"""
import queue


def get_huffman_codes(symbols):
    """Given a list of symbols returns a dict of mappings from
       symbols to codes.
    """
    codes = {}
    root = _create_huffman_tree(symbols)
    _create_codes(codes, root)
    return codes


class _HuffmanNode:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None
        self.code = None

    def __lt__(self, other_node):
        return self.frequency < other_node.frequency

    def __gt__(self, other_node):
        return self.frequency > other_node.frequency

    def __le__(self, other_node):
        return self.frequency <= other_node.frequency

    def __ge__(self, other_node):
        return self.frequency >= other_node.frequency

    def __eq__(self, other_node):
        return self.frequency == other_node.frequency

    def __ne__(self, other_node):
        return self.frequency != other_node.frequency


def _create_huffman_nodes(symbols):
    nodes = []
    for symbol in symbols:
        if any(node.value == symbol for node in nodes):
            for node in nodes:
                if node.value == symbol:
                    node.frequency += 1
                    break
        else:
            nodes.append(_HuffmanNode(symbol, 1))
    return nodes


def _create_huffman_tree(symbols):
    priority_queue = queue.PriorityQueue()
    nodes = _create_huffman_nodes(symbols)
    for node in nodes:
        priority_queue.put(node)

    while priority_queue.qsize() > 1:
        smallest = priority_queue.get()
        next_smallest = priority_queue.get()
        internal_node = _HuffmanNode(None,
                                     smallest.frequency+next_smallest.frequency
                                     )
        internal_node.left = smallest
        internal_node.right = next_smallest
        priority_queue.put(internal_node)

    root = priority_queue.get()
    assert priority_queue.empty()
    return root


def _create_codes(output, node, current_code=''):
    if node.value:
        if current_code:
            node.code = current_code
            output[node.value] = node.code
        else:
            node.code = '0'
            output[node.value] = node.code
    else:
        _create_codes(output, node.left, current_code + '0')
        _create_codes(output, node.right, current_code + '1')


# Define the standard JPEG huffman tables (instead of using my huffman
# methods since JPEG has specific requirements about the codes generated)
JPEG_HUFFMAN_DC_LUM = {0: '00', 1: '010', 2: '011', 3: '100',
                       4: '101', 5: '110', 6: '1110', 7: '11110',
                       8: '111110', 9: '1111110', 10: '11111110',
                       11: '111111110'}


JPEG_HUFFMAN_DC_CHROM = {0: '00', 1: '01', 2: '10', 3: '110', 4: '1110',
                         5: '11110', 6: '111110', 7: '1111110', 8: '11111110',
                         9: '111111110', 10: '1111111110', 11: '11111111110'}


# Maybe just use the same table for both AC luminance and chrominance
# because copying this was a huge pain and the worst use of my time
JPEG_HUFFMAN_AC_LUM = {
    0x00: '1010',
    0x01: '00',
    0x02: '01',
    0x03: '100',
    0x04: '1011',
    0x05: '11010',
    0x06: '1111000',
    0x07: '11111000',
    0x08: '1111110110',
    0x09: '1111111110000010',
    0x0A: '1111111110000011',
    0x11: '1100',
    0x12: '11011',
    0x13: '1111001',
    0x14: '111110110',
    0x15: '11111110110',
    0x16: '1111111110000100',
    0x17: '1111111110000101',
    0x18: '1111111110000110',
    0x19: '1111111110000111',
    0x1A: '1111111110001000',
    0x21: '11100',
    0x22: '11111001',
    0x23: '1111110111',
    0x24: '111111110100',
    0x25: '1111111110001001',
    0x26: '1111111110001010',
    0x27: '1111111110001011',
    0x28: '1111111110001100',
    0x29: '1111111110001101',
    0x2A: '1111111110001110',
    0x31: '111010',
    0x32: '111110111',
    0x33: '111111110101',
    0x34: '1111111110001111',
    0x35: '1111111110010000',
    0x36: '1111111110010001',
    0x37: '1111111110010010',
    0x38: '1111111110010011',
    0x39: '1111111110010100',
    0x3A: '1111111110010101',
    0x41: '111011',
    0x42: '1111111000',
    0x43: '1111111110010110',
    0x44: '1111111110010111',
    0x45: '1111111110011000',
    0x46: '1111111110011001',
    0x47: '1111111110011010',
    0x48: '1111111110011011',
    0x49: '1111111110011100',
    0x4A: '1111111110011101',
    0x51: '1111010',
    0x52: '11111110111',
    0x53: '1111111110011110',
    0x54: '1111111110011111',
    0x55: '1111111110100000',
    0x56: '1111111110100001',
    0x57: '1111111110100010',
    0x58: '1111111110100011',
    0x59: '1111111110100100',
    0x5A: '1111111110100101',
    0x61: '1111011',
    0x62: '111111110110',
    0x63: '1111111110100110',
    0x64: '1111111110100111',
    0x65: '1111111110101000',
    0x66: '1111111110101001',
    0x67: '1111111110101010',
    0x68: '1111111110101011',
    0x69: '1111111110101100',
    0x6A: '1111111110101101',
    0x71: '11111010',
    0x72: '111111110111',
    0x73: '1111111110101110',
    0x74: '1111111110101111',
    0x75: '1111111110110000',
    0x76: '1111111110110001',
    0x77: '1111111110110010',
    0x78: '1111111110110011',
    0x79: '1111111110110100',
    0x7A: '1111111110110101',
    0x81: '111111000',
    0x82: '111111111000000',
    0x83: '1111111110110110',
    0x84: '1111111110110111',
    0x85: '1111111110111000',
    0x86: '1111111110111001',
    0x87: '1111111110111010',
    0x88: '1111111110111011',
    0x89: '1111111110111100',
    0x8A: '1111111110111101',
    0x91: '111111001',
    0x92: '1111111110111110',
    0x93: '1111111110111111',
    0x94: '1111111111000000',
    0x95: '1111111111000001',
    0x96: '1111111111000010',
    0x97: '1111111111000011',
    0x98: '1111111111000100',
    0x99: '1111111111000101',
    0x9A: '1111111111000110',
    0xA1: '111111010',
    0xA2: '1111111111000111',
    0xA3: '1111111111001000',
    0xA4: '1111111111001001',
    0xA5: '1111111111001010',
    0xA6: '1111111111001011',
    0xA7: '1111111111001100',
    0xA8: '1111111111001101',
    0xA9: '1111111111001110',
    0xAA: '1111111111001111',
    0xB1: '1111111001',
    0xB2: '1111111111010000',
    0xB3: '1111111111010001',
    0xB4: '1111111111010010',
    0xB5: '1111111111010011',
    0xB6: '1111111111010100',
    0xB7: '1111111111010101',
    0xB8: '1111111111010110',
    0xB9: '1111111111010111',
    0xBA: '1111111111011000',
    0xC1: '1111111010',
    0xC2: '1111111111011001',
    0xC3: '1111111111011010',
    0xC4: '1111111111011011',
    0xC5: '1111111111011100',
    0xC6: '1111111111011101',
    0xC7: '1111111111011110',
    0xC8: '1111111111011111',
    0xC9: '1111111111100000',
    0xCA: '1111111111100001',
    0xD1: '11111111000',
    0xD2: '1111111111100010',
    0xD3: '1111111111100011',
    0xD4: '1111111111100100',
    0xD5: '1111111111100101',
    0xD6: '1111111111100110',
    0xD7: '1111111111100111',
    0xD8: '1111111111101000',
    0xD9: '1111111111101001',
    0xDA: '1111111111101010',
    0xE1: '1111111111101011',
    0xE2: '1111111111101100',
    0xE3: '1111111111101101',
    0xE4: '1111111111101110',
    0xE5: '1111111111101111',
    0xE6: '1111111111110000',
    0xE7: '1111111111110001',
    0xE8: '1111111111110010',
    0xE9: '1111111111110011',
    0xEA: '1111111111110100',
    0xF0: '11111111001',
    0xF1: '1111111111110101',
    0xF2: '1111111111110110',
    0xF3: '1111111111110111',
    0xF4: '1111111111111000',
    0xF5: '1111111111111001',
    0xF6: '1111111111111010',
    0xF7: '1111111111111011',
    0xF8: '1111111111111100',
    0xF9: '1111111111111101',
    0xFA: '1111111111111110'
    }
