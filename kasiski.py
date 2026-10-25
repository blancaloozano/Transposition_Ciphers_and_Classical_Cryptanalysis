def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:

    clean = []
    for char in ciphertext.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean.append(char)
    ciphertext = "".join(clean)

    seq_positions = {}

    for length in range(min_len, len(ciphertext)):
        current_seqs = {}
        for i in range(len(ciphertext) - length +1):
            seq = ciphertext[i: i+length]
            if seq not in seq_positions:
                seq_positions[seq] = []
            seq_positions[seq].append(i)

        added_any = False
        for seq, pos in seq_positions.items():
            if len(pos) > 1:
                seq_positions[seq] = pos
                added_any = True

        if not added_any:
            break

    return seq_positions

def distances(ciphertext: str, min_len: int = 3) -> list[int]:

    reps = repeats(ciphertext, min_len)
    dist_list = []

    for positions in reps.values():
        for i in range(len(positions) -1):
            dist = positions[i+1] - positions[i]
            dist_list.append(dist)

    return dist_list

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

# print(repeats("ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO " \
# "PXDOL ELQYR JXAOA LPKGV D"))
    # Output: {'ELQ': [0, 15, 50], 'LQY': [1, 51], 'QYR': [2, 52], 
    # 'YRJ': [3, 53], 'ELQY': [0, 50], 'LQYR': [1, 51], 'QYRJ': [2, 52],
    # 'ELQYR': [0, 50], 'LQYRJ': [1, 51], 'ELQYRJ': [0, 50]}

# print(distances("ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO " \
# "PXDOL ELQYR JXAOA LPKGV D"))
    # Output: [15, 35, 50]