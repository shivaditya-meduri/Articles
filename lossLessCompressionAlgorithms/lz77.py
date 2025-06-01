def lz77_compress(data: bytes, window_size: int = 256) -> list[tuple[int, int, int]]:
    """
    Returns a list of (distance, length, next_byte) tuples.
    If `next_byte` is None (we use -1 here), it means we matched until the very end.
    """
    i = 0
    tokens: list[tuple[int, int, int]] = []
    n = len(data)

    while i < n:
        best_distance = 0
        best_length = 0
        start_window = max(0, i - window_size)

        # Search for longest match in window
        for j in range(start_window, i):
            length = 0
            # Extend match as far as possible
            while i + length < n and data[j + length] == data[i + length]:
                length += 1
            if length > best_length:
                best_length = length
                best_distance = i - j

        # If we found a nonzero-length match:
        if best_length > 0:
            next_byte = data[i + best_length] if (i + best_length) < n else -1
            tokens.append((best_distance, best_length, next_byte))
            i += best_length + 1
        else:
            # No match, emit a literal (distance=0, length=0, next_byte=data[i])
            tokens.append((0, 0, data[i]))
            i += 1

    return tokens


def lz77_decompress(tokens: list[tuple[int, int, int]]) -> bytes:
    """
    Consume tokens of the form (distance, length, next_byte).
    If next_byte is -1, it means “no literal follow; we matched exactly to the end.”
    """
    out = bytearray()

    for distance, length, next_byte in tokens:
        if distance > 0 and length > 0:
            start = len(out) - distance
            # Copy `length` bytes from `start`
            for k in range(length):
                out.append(out[start + k])
        if next_byte != -1:
            out.append(next_byte)

    return bytes(out)


if __name__ == "__main__":
    # Example usage:
    original = b"ABAABA"
    tokens = lz77_compress(original, window_size=4)
    print("Tokens:", tokens)
    restored = lz77_decompress(tokens)
    print("Restored:", restored)
