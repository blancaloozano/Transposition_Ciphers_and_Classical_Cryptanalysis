
from affine import encrypt, decrypt, valid_keys
from break_caesar import chi_squared, english, spanish

def break_affine(ciphertext: str, language: str = "en") -> tuple[tuple[int, int], str]:
    
    if language == 'en':
        table = english
    else:
        table = spanish

    best_key = (0,0)
    best_score = float('inf')
    best_plaintext = ""

    for a,b in valid_keys():
        candidate = decrypt(ciphertext, a,b)
        score = chi_squared(candidate, table)

        if score < best_score:
            best_score = score
            best_key = (a,b)
            best_plaintext = candidate

    return (best_key, best_plaintext)

