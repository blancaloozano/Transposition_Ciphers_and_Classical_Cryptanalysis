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

# - HELPER FUNCTION-- Choosing the threshold

def threshold():
    text = reference_en[:400]

    t_cipher = columnar_encrypt(text, "KEYWORD", pad= "X")
    t_score = chi_squared(t_cipher, english)

    s_cipher = monoalphabetic_encrypt(text, get_random_mono_key())
    s_score = chi_squared(s_cipher, english)

    print(f"\nchi-square transposition: {t_score}")
    print(f"chi-square substitution: {s_score}")
    print(f"Middle point: {(t_score + s_score) / 2}")

def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""

    if language == "es":
        table = spanish
    else:
        table = english

    score = chi_squared(ciphertext, table)
    threshold = 6.79

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
    threshold()
    run_measurement(probabilistic_padding=False)
    run_measurement(probabilistic_padding=True)
