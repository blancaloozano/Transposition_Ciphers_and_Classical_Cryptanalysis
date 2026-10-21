
from basics import to_numbers, to_letters

def encrypt(plaintext: str, k: int) -> str:
    nums = to_numbers(plaintext)
    shifted = []

    for n in nums:
        shifted.append((n + k) % 26)

    return to_letters(shifted)


def decrypt(ciphertext: str, k: int) -> str:
    nums = to_numbers(ciphertext)
    shifted = []

    for n in nums:
        shifted.append((n - k) % 26)

    return to_letters(shifted)

