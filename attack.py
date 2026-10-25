import argparse
import sys

from practice1_code.assist import report
from keylength import find_key_length
from measure import classify, index_of_coincidence as ic
from break_columnar import attack as break_columnar_attack
from break_vigenere import attack as break_vigenere_attack

def main():
    parser = argparse.ArgumentParser(description="Automated Cryptanalysis Attack")
    parser.add_argument("--in", dest="input_file", required=True, help="Path to ciphertext file")
    parser.add_argument("--lang", choices=["en", "es"], default="en", help="Target language (default: en)")
    parser.add_argument("--cols", type=int, default=None, help="Number of columns for columnar transposition")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r") as f:
            ciphertext = f.read().strip().upper()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    if not ciphertext:
        print("Error: Ciphertext is empty")
        sys.exit(1)

    cipher_type = classify(ciphertext, language=args.lang)
    text_ic = ic(ciphertext)

    print("\n--- Cryptanalysis Measurements ---\n")
    print(f"Input file: {args.input_file}")
    print(f"Text length: {len(ciphertext)} characters")
    print(f"Index of coincidence (IC): {text_ic:.4f}")
    print(f"Cipher Family: {cipher_type.upper()}\n")
    print("--------------------------------\n")

    if cipher_type == "substitution":

        if text_ic >= 0.05:
            print(f"Substitution type: MONOALPHABETIC (High IC)\n")
            print(report(ciphertext, language= args.lang))

        else:
            print("Substitution type: POLYALPHABETICC / VIGÈNERE (Low IC)")

            guessed_kl = find_key_length(ciphertext, language=args.lang)
            print(f"Estimated key length: {guessed_kl}")

            key, plaintext = break_vigenere_attack(ciphertext, language= args.lang)
            print(f"Recovered Key: {key}")
            print(f"Plaintext:\n\n{plaintext}\n")

    elif cipher_type == "transposition":
        print(f"Cipher type: COLUMNAR")

        if args.cols is not None:
            cols_order, plaintext = break_columnar_attack(ciphertext, n_cols=args.cols, language=args.lang)
            print(f"Column Order: {cols_order}")
            print(f"Plaintext:\n\n{plaintext}\n")

        else:
            print("No --cols N provided. Testing column divisors (2 to 8)")

            best_order = None
            best_plaintext = ""
            best_n = None
            text_len = len(ciphertext)

            divisors = [n for n in range(2,9) if text_len % n == 0]
            if not divisors:
                divisors = list(range(2,9))

            for n in divisors:
                order, candidate = break_columnar_attack(ciphertext, n, language=args.lang)

                if best_n is None:
                    best_n = n
                    best_order = order
                    best_plaintext = candidate

            print(f"Best Column Count: {best_n}")
            print(f"Column order: {best_order}")
            print(f"Plaintext: {best_plaintext}")

if __name__ == "__main__":
    main()