
from basics import to_numbers

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt(plaintext: str, key: str) -> str:
    key = key.upper()

    if len(key) != 26 or set(key) != set(alphabet):
        raise ValueError("Invalid Key.")

    nums = to_numbers(plaintext)
    result = []

    for n in nums:
        result.append(key[n])

    return "".join(result)

def decrypt(ciphertext: str, key: str) -> str:
    key = key.upper()
    
    if len(key) != 26 or set(key) != set(alphabet):
        raise ValueError("Invalid Key.")

    result = []
    for char in ciphertext:
        if char in key:
            original_num = key.index(char)
            result.append(alphabet[original_num])
    
    return "".join(result)

def key_from_keyword(keyword: str) -> str:
    key_chars = []

    for char in keyword.upper():
        if char in alphabet and char not in key_chars:
            key_chars.append(char)

    for char in alphabet:
        if char not in key_chars:
            key_chars.append(char)

    return "".join(key_chars)
