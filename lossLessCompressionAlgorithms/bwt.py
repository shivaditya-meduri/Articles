def bwt(s: str) -> tuple[str, int]:
    """Applies the Burrows-Wheeler Transform to a string."""
    if not s:
        return "", -1
    s_with_eof = s + '\0'  # Add an End-Of-File marker (can be any char not in s)
    rotations = sorted([s_with_eof[i:] + s_with_eof[:i] for i in range(len(s_with_eof))])
    bwt_string = "".join([r[-1] for r in rotations])
    original_index = rotations.index(s_with_eof)
    return bwt_string, original_index

def inverse_bwt(bwt_string: str, original_index: int) -> str:
    """Reverses the Burrows-Wheeler Transform."""
    if not bwt_string:
        return ""
    table = [""] * len(bwt_string)
    for _ in range(len(bwt_string)):
        table = sorted([bwt_string[i] + table[i] for i in range(len(bwt_string))])
    original_string_with_eof = table[original_index]
    return original_string_with_eof.rstrip('\0') # Remove EOF marker

# Example data stream
data = "banana"


bwtstr, orig_ind = bwt(data)

print(f"BWT string : {bwtstr} | Original Index : {orig_ind}")