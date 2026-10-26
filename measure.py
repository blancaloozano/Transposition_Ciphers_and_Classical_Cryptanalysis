import random
from collections import Counter
from columnar import encrypt as columnar_encrypt

# Reusing the Practice 1 code:
from practice1_code.break_caesar import chi_squared, english, spanish, reference_en
from practice1_code.monoalpha import encrypt as monoalphabetic_encrypt, key_from_keyword


# B1 - Index of Coincidence

def index_of_coincidence(text: str) -> float:

    clean = []
    for char in text.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean.append(char)
    text = "".join(clean)

    n = len(text)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numerator = 0

    if len(text) < 2:
        return 0.0

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

# print(index_of_coincidence(reference_en))
    # Output: 0.06363493619531406

# Código temporal para sacar los datos del informe
print("Length   | IC")
print("-----------------------")
for length in [20, 50, 100, 200, 400]:
    ic_val = index_of_coincidence(reference_en[:length])
    print(f"{length:<8} | {ic_val:.4f}")

# B2 - Cipher Family Classifier

def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""

    if language == "es":
        table = spanish
    else:
        table = english

    score = chi_squared(ciphertext, table)
    threshold = 1.0

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

# Threshold Selection

def threshold(samples: int = 1500, thresholds = None):

    if thresholds is None:
        thresholds = [0.5, 0.7, 1.0, 1.5, 2.0, 3.0]

    lengths = [60, 120, 250, 400]

    scores_x = []       # transposition, fixed padding X
    scores_rand = []    # transposition, probabilistic padding
    scores_sub = []     # monoalphabetic substitution

    for L in lengths:
        plaintext = reference_en[0:L]

        for i in range(samples):
            key = get_random_columnar_key()

            c_x = columnar_encrypt(plaintext, key, pad="X")
            scores_x.append(chi_squared(c_x, english))

            pad_char = get_probabilistic_pad(english)
            c_r = columnar_encrypt(plaintext, key, pad=pad_char)
            scores_rand.append(chi_squared(c_r, english))

            c_s = monoalphabetic_encrypt(plaintext, get_random_mono_key())
            scores_sub.append(chi_squared(c_s, english))

    print(f"\n--- Threshold selection ({samples} samples per length and cipher) ---")
    print("t    | Transposition errors, X pad | Transposition errors, random pad | Substitution errors")
    print("-" * 95)

    for t in thresholds:
        err_x = sum(1 for v in scores_x if v >= t) / len(scores_x) * 100
        err_r = sum(1 for v in scores_rand if v >= t) / len(scores_rand) * 100
        err_s = sum(1 for v in scores_sub if v < t) / len(scores_sub) * 100
        print(f"{t:<4} | {err_x:>26.1f}% | {err_r:>31.1f}% | {err_s:>18.2f}%")


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

        # 150 Substitution trials
        for i in range(150):
            key = get_random_mono_key()
            ciphertext = monoalphabetic_encrypt(plaintext, key)

            if classify(ciphertext, "en") != "substitution":
                substitution_errors += 1

        total_errors = substitution_errors + transposition_errors
        error_rate = (total_errors / 300) * 100 
        print(f"{L:<6} | {transposition_errors:<12} | {substitution_errors:<12} | {error_rate:.2f}%")

if __name__ == "__main__":
    # threshold() # We don't want the table from generating for every analysis, so I see it and # it.
    run_measurement(probabilistic_padding=False)
    run_measurement(probabilistic_padding=True)
