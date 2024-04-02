import heapq
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(None, left_child.freq + right_child.freq)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]


def build_huffman_codes(node, prefix="", code=None):
    if code is None:
        code = {}
    if node is not None:
        if node.char is not None:
            code[node.char] = prefix
        build_huffman_codes(node.left, prefix + "0", code)
        build_huffman_codes(node.right, prefix + "1", code)
    return code


def huffman_compress(text, output_file):
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = ''.join([codes[char] for char in text])
    padding = 8 - len(encoded_text) % 8
    encoded_text = '{:08b}'.format(padding) + encoded_text + '0' * padding

    with open(output_file, 'wb') as f:
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            f.write(bytes([int(byte, 2)]))


def huffman_decompress(input_file):
    with open(input_file, 'rb') as f:
        byte = f.read(1)
        padding = int.from_bytes(byte, byteorder='big')
        encoded_text = ''
        while byte != b"":
                byte = f.read(1)
                if byte == b"":
                    break
                encoded_text += '{:08b}'.format(ord(byte))

    encoded_text = encoded_text[:-padding]
    decoded_text = ""
    node = build_huffman_tree(text)
    current_node = node
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = node

    return decoded_text


# Приклад використання:
text = "Приклад тексту для роботи програми"
output_file = "compressed.bin"
huffman_compress(text, output_file)
print("файл успішно ущільнено.")

decompressed_text = huffman_decompress(output_file)
print("розшифрований файл:", decompressed_text)