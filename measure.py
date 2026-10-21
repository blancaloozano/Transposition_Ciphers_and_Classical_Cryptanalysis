import random
from collections import Counter
from columnar import encrypt as columnar_encrypt

# Reusing the Practice 1 code:
from practice1_code.break_caesar import chi_squared, english, spanish, reference_en
from practice1_code.monoalpha import encrypt as monoalphabetic_encrypt


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

def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""

    if language == "es":
        table = spanish
    else:
        table = english

    score = chi_squared(ciphertext, table)
    threshold = 0.035

    if score < threshold:
        return "transposition"
    else:
        return "substitution"

# Measurement Task

def get_random_columnar_key() -> str:
    "Generates a random keyword of length between 4 and 8."
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key_len = random.randint(4,8)
    key = ""

    for i in range(key_len):
        key += random.choice(alphabet)

    return key

def get_random_mono_key() -> str:
    "Generates a random 26-letter substitution key."

    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    return alphabet
    # key_len = random.randint(4,8)
    # key = ""

    # for i in range(key_len):
    #     key += random.choice(alphabet)

    # return key

print(get_random_mono_key())




