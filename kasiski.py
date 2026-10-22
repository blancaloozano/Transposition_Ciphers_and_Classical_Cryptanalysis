def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:

    ciphertext = ciphertext.replace(" ", "")

    seq_positions = {}

    # We want to extract all sub-sequences of length >= min_len
    for length in range(min_len, len(ciphertext)):
        for i in range(len(ciphertext) - length +1):
            seq = ciphertext[i: i+length]
            if seq not in seq_positions:
                seq_positions[seq] = []
            seq_positions[seq].append(i)

    repeats_dict = {}

    for seq, pos in seq_positions.items():
        if len(pos) > 1:
            repeats_dict[seq] = pos

    return repeats_dict

def distances(ciphertext: str, min_len: int = 3) -> list[int]:

    reps = repeats(ciphertext, min_len)
    distances = set()

    for positions in reps.values():
        for i in range(len(positions)):
            for j in range(i +1, len(positions)):
                dist = positions[j] - positions[i]
                distances.add(dist)

    return sorted(list(distances))

def factor_tally(ciphertext: str, max_factor: int = 20) -> dict[int, int]:

    dists = distances(ciphertext)
    tally = {}

    for f in range(2, max_factor + 1):
        tally[f] = 0

    for d in dists:
        for f in range(2, max_factor +1):
            if d % f == 0:
                tally[f] += 1

    return tally
