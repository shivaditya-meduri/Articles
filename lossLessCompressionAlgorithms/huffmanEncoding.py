import heapq
from collections import Counter

# Node class for Huffman tree
class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    # Comparison method for priority queue (heapq)
    def __lt__(self, other):
        return self.freq < other.freq

# Function to build Huffman tree from input data
def build_huffman_tree(data):
    freq = Counter(data)
    heap = [Node(f, sym) for sym, f in freq.items()]
    heapq.heapify(heap)

    # Merge nodes until one tree remains
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

# Function to generate Huffman codes from the tree
def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.symbol is not None:
        # Leaf node: assign prefix as the code for this symbol
        codebook[node.symbol] = prefix
    else:
        # Internal node: traverse left and right
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

# Function to encode data using the codebook
def encode(data, codebook):
    return "".join(codebook[symbol] for symbol in data)

# Function to decode the encoded bitstring using the Huffman tree
def decode(encoded, tree):
    decoded = []
    node = tree
    for bit in encoded:
        node = node.left if bit == "0" else node.right
        if node.symbol is not None:
            decoded.append(node.symbol)
            node = tree
    return "".join(decoded)

# Example data stream
data = "abbccc"

# Build tree and generate codes
tree = build_huffman_tree(data)
codes = generate_codes(tree)

# Display the code for each symbol
print("Huffman Codes for each symbol:", codes)

# Encode the data stream
encoded = encode(data, codes)
print("Encoded bitstring:", encoded)

# Decode back to verify correctness
decoded = decode(encoded, tree)
print("Decoded string:", decoded)
