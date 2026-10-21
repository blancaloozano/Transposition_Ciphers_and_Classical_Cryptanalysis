# B1 - Index of Coincidence

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


# B2 - Cipher Family Classifier

# Reusing The chi-square function and frequency tables we defined in Lab 1:


english = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
           'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
           'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
           'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
           'Y': 0.01974, 'Z': 0.00074
}

spanish = {'A': 0.11525, 'B': 0.02215, 'C': 0.04019, 'D': 0.05010, 'E': 0.13702, 'F': 0.00692,
           'G': 0.01768, 'H': 0.01973, 'I': 0.06247, 'J': 0.00493, 'K': 0.00026, 'L': 0.04967,
           'M': 0.03157, 'N': 0.06712, 'O': 0.08683, 'P': 0.02510, 'Q': 0.00877, 'R': 0.06871,
           'S': 0.07977, 'T': 0.04632, 'U': 0.03927, 'V': 0.01138, 'W': 0.00027, 'X': 0.00515,
           'Y': 0.01433, 'Z': 0.00467
}

def chi_squared(text: str, table: dict[str, float]) -> float:
    length = len(text)
    if length == 0:
        return float('inf')

    counts = Counter(text)
    chi_sq = 0.0

    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        obs = counts.get(char, 0)
        expected = length * table.get(char, 0.0)

        if expected > 0:
            chi_sq += ((obs - expected) **2) / expected

    return chi_sq / length

# def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""

