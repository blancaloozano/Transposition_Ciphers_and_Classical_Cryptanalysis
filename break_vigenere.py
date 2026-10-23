import random
from keylength import find_key_length

from practice1_code.break_caesar import break_caesar, reference_en
from practice1_code.vigenere import decrypt as vigenere_decrypyt, cosets as get_cosets, encrypt as vigenere_encrypt

def attack(ciphertext: str, language: str = "en") -> tuple[str, str]:
    """Returns (key,plaintext). The key length is NOT given"""

    kl = find_key_length(ciphertext, language=language)
    cosets = get_cosets(ciphertext, kl)

    key = ""
    for coset in cosets:
        best_shift, _ = break_caesar(coset, language)
        key += chr(best_shift + 65)

    plaintext = vigenere_decrypyt(ciphertext, key)

    return key, plaintext

# Measurement Task - Report 

# Helper Functions

def get_random_key(length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = ""
    for i in range(length):
        key += random.choice(alphabet)

    return key

def run_measurement():
    key_lengths = [3, 5, 7, 9]
    text_lengths = [100, 150, 200, 300, 400]
    trials = 100

    long_reference = reference_en * 5

    table1_results = {}
    table2_results = {}

    for L in text_lengths:
        table1_results[L] = {}
        table2_results[L] = {}
        for K in key_lengths:
            full_key_successes = 0
            len_successes = 0
            for i in range(trials):
                start_idx = random.randint(0, len(reference_en) - L)
                plaintext = long_reference[start_idx : start_idx + L]
                true_key = get_random_key(K)

                ciphertext = vigenere_encrypt(plaintext, true_key)

                if find_key_length(ciphertext) == K:
                    len_successes +=1

                guessed_key, _ = attack(ciphertext)
                if guessed_key == true_key:
                    full_key_successes +=1

            table1_results[L][K] = (full_key_successes / trials) *100
            table2_results[L][K] = (len_successes / trials) *100
    
    print("\n--- Table 1: Complete Key Recovery Rate (%) ---")
    print(f"{'Length':<8} | {'K=3':<6} | {'K=5':<6} | {'K=7':<6} | {'K=9':<6}")
    print("-"*45)

    for L in text_lengths:
            r = table1_results[L]
            print(f"{L:<8} | {r[3]:>5.0f}% | {r[5]:>5.0f}% | {r[7]:>5.0f}% | {r[9]:>5.0f}%")

    print("\n--- Table 2: Key Length Recovery Rate (%) ---")
    print(f"{'Length':<8} | {'K=3':<6} | {'K=5':<6} | {'K=7':<6} | {'K=9':<6}")
    print("-"*45)

    for L in text_lengths:
        r = table2_results[L]
        print(f"{L:<8} | {r[3]:>5.0f}% | {r[5]:>5.0f}% | {r[7]:>5.0f}% | {r[9]:>5.0f}%")

if __name__ == "__main__":
    run_measurement()