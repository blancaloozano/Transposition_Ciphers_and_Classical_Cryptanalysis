import random
from keylength import find_key_length

from practice1_code.break_caesar import break_caesar, reference_en
from practice1_code.vigenere import decrypt as vigenere_decrypyt, cosets as get_cosets


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

# def run_measurement():
#     key_lengths = [3, 5, 7, 9]
#     text_lengths = [1, 150, 200, 300, 400]
#     trials = 100

#     reference = reference_en * 5

#     full_key_results = {}
#     len_only_results = {}

#     for L in text_lengths:
#         full_key_results[L] = {}
#         len_only_results[L] = {}
#         for K in key_lengths:
#             full_key_results[L][K] = 0
#             len_only_results[L][K] = 0
    
