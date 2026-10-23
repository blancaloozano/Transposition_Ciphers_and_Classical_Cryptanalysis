
from .basics import to_numbers, to_letters

def encrypt(plaintext: str, key: str) -> str:
    
    if not key or not key.isalpha():
        raise ValueError('Invalid Key. It cannot be empty and must contain only alphabetic characters')

    p_nums = to_numbers(plaintext)
    k_nums = to_numbers(key)
    result = []
    key_len = len(k_nums)

    for i in range(len(p_nums)):
        shift = k_nums[i % key_len]
        result.append((p_nums[i] + shift) % 26)

    return to_letters(result)

def decrypt(ciphertext: str, key: str) -> str:

    if not key or not key.isalpha():
        raise ValueError('Invalid Key. It cannot be empty and must contain only alphabetic characters')

    c_nums = to_numbers(ciphertext)
    k_nums = to_numbers(key)
    result = []
    key_len = len(k_nums)

    for i in range(len(c_nums)):
        shift = k_nums[i % key_len]
        result.append((c_nums[i] - shift) % 26)

    return to_letters(result)

def cosets(ciphertext: str, m: int) -> list[str]:
    normalised = to_letters(to_numbers(ciphertext))
    result = [""] * m

    for i in range(len(ciphertext)):
        result[i % m] += ciphertext[i]

    return result