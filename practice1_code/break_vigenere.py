
from vigenere import cosets, decrypt
from break_caesar import break_caesar

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def break_vigenere(ciphertext: str, m: int, language: str = "en") -> tuple[str, str]:
    """ m is the key length, given to you. Return (key, plaintext)."""

    text_cosets = cosets(ciphertext, m)
    key_chars = []

    for coset in text_cosets:
        shift, i = break_caesar(coset, language)
        key_chars.append(alphabet[shift])

    found_key = "".join(key_chars)
    found_plaintext = decrypt(ciphertext, found_key)

    return (found_key, found_plaintext)
