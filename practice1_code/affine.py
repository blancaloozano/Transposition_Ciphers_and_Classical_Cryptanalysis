
from basics import to_numbers, to_letters, egcd, modinv


def encrypt(plaintext: str, a: int, b:int) -> str:
    g, i, i = egcd(a, 26)

    if g != 1:
        raise ValueError(f"Invalid key. a {a} is not invertible mod 26")
        
    nums = to_numbers(plaintext)
    result = []

    for x in nums:
        result.append((a * x + b) % 26)
        
    return to_letters(result)

def decrypt(ciphertext: str, a: int, b: int) -> str:
    g, i, i = egcd(a, 26)

    if g != 1:
        raise ValueError(f"Invalid key. a {a} is not invertible mod 26")

    a_inv = modinv(a,26)

    nums = to_numbers(ciphertext)
    result = []

    for y in nums:
        result.append((a_inv * (y - b)) % 26)
        
    return to_letters(result)
    

def valid_keys() -> list [tuple[int, int]]:
    keys = []

    for a in range(26):
        g, i, i = egcd(a, 26)
        if g == 1:
            for b in range(26):
                keys.append((a,b))

    return keys
