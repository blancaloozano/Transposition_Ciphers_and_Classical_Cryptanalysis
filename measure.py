import random
from collections import Counter
from columnar import encrypt as columnar_encrypt

# Reusing the Practice 1 code:
from practice1_code.break_caesar import chi_squared, english, spanish, reference_en
from practice1_code.monoalpha import encrypt as monoalphabetic_encrypt, key_from_keyword


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

# Measurement Task - Report 

# Helper Functions

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
    random.shuffle(alphabet)

    key = ""
    for char in alphabet:
        key += char

    return key

def get_probabilistic_pad(table: dict[str, float]) -> str:
    "Selects a pad character randomly based on language frequencies."

    letters = list(table.keys())
    weights = list(table.values())
    chosen = random.choices(letters, weights, k = 1)
    return chosen[0]

# Execution

def run_measurement(probabilistic_padding: bool = False):
    lengths = [60, 120, 250, 400]

    if probabilistic_padding:
        print(f"\n--- Table 2: Probabilistic Padding ---")
    else:
        print(f"\n--- Table 1: Fixed Padding (X) ---")

    print("Length | Transposition Errors | Substitution Errors | Total Errors")
    print("-"* 55)

    for L in lengths:
        plaintext = reference_en[0:L]
        transposition_errors = 0
        substitution_errors = 0

        # 150 Transposition trials
        for i in range(150):
            key = get_random_columnar_key()
            if probabilistic_padding:
                pad_char = get_probabilistic_pad(english)
            else:
                pad_char = "X"

            ciphertext = columnar_encrypt(plaintext, key, pad = pad_char)
            if classify(ciphertext, "en") != "transposition":
                transposition_errors += 1

        # 150 Transposition trials
        for i in range(150):
            key = get_random_mono_key()
            ciphertext = monoalphabetic_encrypt(plaintext, key)

            if classify(ciphertext, "en") != "substitution":
                substitution_errors += 1

        total_errors = substitution_errors + transposition_errors
        error_rate = (total_errors / 300) * 100 
        print(f"{L:<6} | {transposition_errors:<12} | {substitution_errors:<12} | {error_rate:.2f}%")

if __name__ == "__main__":
    run_measurement(probabilistic_padding=False)
    run_measurement(probabilistic_padding=True)
