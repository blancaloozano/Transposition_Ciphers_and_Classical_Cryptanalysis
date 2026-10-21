def index_of_coincidence(text: str) -> float:
    n = len(text)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numerator = 0

    # We calculte the frequency for every letter in the text
    for letter in alphabet:
        count = 0
        for character in text:
            if letter == character:
                count += 1

        numerator += count *(count - 1)
    denominator = n * (n -1)

    return numerator / denominator

# print(index_of_coincidence("CRYPTANALYSIS"))
    # Output: 0.038461538461538464

# def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""

