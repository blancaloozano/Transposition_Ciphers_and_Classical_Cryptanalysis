import argparse
import sys

from measure import classify
from break_columnar import attack as break_columnar_attack
from break_vigenere import attack as break_vigenere_attack


def main():
    parser = argparse.ArgumentParser(description="Automated Cryptanalysis Attack")

    parser.add_argument("--in", dest="input_file", required=True, help="Path to ciphertext file")
    parser.add_argument("--lang", choices=["en", "es"], default="en", help="Target language (default: en)")
    parser.add_argument("--cols", type=int, default=None, help="Number of columns for columnar transposition")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            ciphertext = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    if not ciphertext:
        print("Error: Ciphertext is empty")
        sys.exit(1)

    cipher_type = classify(ciphertext, language=args.lang)

    if cipher_type == "substitution":
        key, plaintext = break_vigenere_attack(ciphertext, language=args.lang)
        print(f"Recovered Key: {key}")
        print(f"Plaintext:\n{plaintext}")

    elif cipher_type == "transposition":
        if args.cols is None:
            print("Error: Transposition detected but --cols N was not provided.")
            sys.exit(1)

        cols_order, plaintext = break_columnar_attack(ciphertext, n_cols=args.cols, language=args.lang)
        print(f"Column Order: {cols_order}")
        print(f"Plaintext:\n{plaintext}")

if __name__ == "__main__":
    main()