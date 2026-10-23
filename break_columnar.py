import time
import random
import math
from itertools import permutations
from collections import Counter

from columnar import encrypt as columnar_encrypt
from practice1_code.break_caesar import reference_en

def attack(ciphertext: str, n_cols: int, language: str = "en") -> tuple[tuple[int, ...], str]:
    """Returns (column order, plaintext) for a known number of columns."""

    text = reference_en
    bigrams = []
    for i in range(len(text) -1):
        pair = text[i: i+2]
        if len(pair) == 2:
            bigrams.append(pair)

    counts = Counter(bigrams)
    total = sum(counts.values())

    log_probs = {}
    min_prob = math.log10(0.01 / total)
    for bg, count in counts.items():
        log_probs[bg] = math.log10(count / total)

    rows = len(ciphertext) // n_cols
    columns = []
    for i in range(n_cols):
        col_str = ciphertext[i * rows : (i + 1) * rows]
        columns.append(col_str)

    best_score = -float("inf")
    best_plaintext = ""
    best_order = None    

    for order in permutations(range(n_cols)):
        plaintext_chars = []
        for r in range(rows):
            for col_idx in order:
                plaintext_chars.append(columns[col_idx][r])

        candidate = "".join(plaintext_chars)

        current_score = 0.0
        for i in range(len(candidate) - 1):
            bg = candidate[i : i + 2]
            current_score += log_probs.get(bg, min_prob)

        if current_score > best_score:
            best_score = current_score
            best_plaintext = candidate
            best_order = order

    return best_order, best_plaintext


# Measurement Task

# Helper functions

def get_random_keyword(length: int) -> str:
    """Generates a random keyword with distinct letters."""
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(alphabet)
    key = ""
    for i in range(length):
        key += alphabet[i]
    return key

def run_measurement():
    cols_list = [4, 5, 6, 7]
    lens_list = [60, 120, 200]
    trials = 100

    long_reference = reference_en * 3
    table_results = {}

    for L in lens_list:
        table_results[L] = {}
        for C in cols_list:
            successes = 0
            for i in range(trials):
                start = random.randint(0, len(reference_en) - L - 1)
                raw_plaintext = long_reference[start : start + L]

                key = get_random_keyword(C)
                ciphertext = columnar_encrypt(raw_plaintext, key, pad="X")

                expected_plain = raw_plaintext
                padding = len(raw_plaintext) % C
                if padding != 0:
                    expected_plain += "X" * (C - padding)

                _, recovered_text = attack(ciphertext, C)

                if recovered_text == expected_plain:
                    successes += 1

            table_results[L][C] = (successes / trials) * 100

    print("\n--- Table: Columnar Breaker Success Rate (%) ---")
    print(f"{'Length':<8} | {'N=4':<6} | {'N=5':<6} | {'N=6':<6} | {'N=7':<6}")
    print("-" * 45)

    for L in lens_list:
        r = table_results[L]
        print(f"{L:<8} | {r[4]:>5.0f}% | {r[5]:>5.0f}% | {r[6]:>5.0f}% | {r[7]:>5.0f}%")

def test_performance_limit():
    print("\n--- Performance Limit Test ---")
    n_cols = 7
    while True:
        key = get_random_keyword(n_cols)
        plaintext = reference_en[:60]
        ciphertext = columnar_encrypt(plaintext, key)

        start_time = time.time()
        attack(ciphertext, n_cols)
        elapsed = time.time() - start_time

        print(f"Columns (N={n_cols}) -> Time: {elapsed:.3f} seconds")
        if elapsed > 10.0:
            print(f"Limit reached! Largest N under 10 seconds is {n_cols - 1}.")
            break
        n_cols += 1


if __name__ == "__main__":
    run_measurement()
    test_performance_limit()