from collections import Counter
from .basics import to_numbers, to_letters
from .break_caesar import english, spanish

def report(ciphertext: str, language: str = "en") -> str:

    if language == 'en':
        table = english
    else:
        table = spanish

    ciphertext = to_letters(to_numbers(ciphertext))

    length = len(ciphertext)
    if length == 0:
        return "The ciphertext is empty"

    output = []


    # 1. Letter Frequency
    output.append('1. Letter frequency')
    counts = Counter(ciphertext)
    ranked_cipher = counts.most_common()

    ranked_expected = sorted(table.items(), key = lambda x: x[1], reverse = True)
    output.append("-" * 47)

    for i in range(len(ranked_cipher)):
        c_char, c_count = ranked_cipher[i]
        c_pct = (c_count / length) * 100

        e_char, e_pct = ("", 0.0)
        if i < len(ranked_expected):
            e_char = ranked_expected[i][0]
            e_pct = ranked_expected[i][1]* 100

        output.append(f"   {c_char:<4} | {c_count:<5} | {c_pct:<5.2f}% ||    {e_char:<5} | {e_pct:<5.2f}%")

        
    # 2. Repeated Trigrams            
    output.append('2. Repeated Trigrams')
    trigrams = {}
    for i in range(length - 2):
        tri = ciphertext[i:i+3]
        trigrams.setdefault(tri, []).append(i)
        
    repeated_trigrams = {k: v for k, v in trigrams.items() if len(v) > 1}
    sorted_tri = sorted(repeated_trigrams.items(), key=lambda x: len(x[1]), reverse=True)

    if sorted_tri:
        for tri, positions in sorted_tri:
            pos_str = ", ".join(str(p) for p in positions)
            output.append(f"   {tri}  x{len(positions)}  at positions: {pos_str}")
    else:
        output.append("No repeated trigrams found.")        


    # 3. Ten most frequent bigrams
    output.append("3. Ten most frequent bigrams")
    bigram_counts = Counter(ciphertext[i:i+2] for i in range(length - 1))
    top_bigrams = bigram_counts.most_common(10)
    if top_bigrams:
        for bigram, count in top_bigrams:
            output.append(f"   {bigram}  x{count}")
    else:
        output.append("   Ciphertext too short for bigrams.")

    # 4. Doubled Letters
    output.append("4. Doubled letters")
    doubles = []
    for i in range(length - 1):
        if ciphertext[i] == ciphertext[i+1]:
            doubles.append((ciphertext[i:i+2], i))

    if doubles:
        for pair, pos in doubles:
            output.append(f"   {pair}  at position {pos}")
    else:
        output.append("   No double letters found.")

    # 5. Suggested Initial Mapping
    output.append("5. Initial suggested mapping")
    mapping = {}
    for i in range(len(ranked_cipher)):
        if i < len(ranked_expected):
            mapping[ranked_cipher[i][0]] = ranked_expected[i][0]

    found_letters = sorted(mapping.keys())
    output.append("Cipher Letter:    " + " ".join(found_letters))
    output.append("Suggested Letter: " + " ".join(mapping[letra] for letra in found_letters))

    return "\n".join(output)