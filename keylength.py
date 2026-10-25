from measure import index_of_coincidence
from practice1_code.break_caesar import reference_en
from practice1_code.vigenere import encrypt as vigenere_encrypt


def coset_ic(ciphertext: str, m: int) -> float :
    "Splits the ciphertext into m cosets and returns the average"
    "of their indices."

    clean = []
    for char in ciphertext.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean.append(char)
    ciphertext = "".join(clean)
    
    cosets = []
    for i in range(m):
        cosets.append("")

    for i in range(len(ciphertext)):
        coset_index = i % m
        cosets[coset_index] += ciphertext[i]

    total_ic = 0
    for coset in cosets:
        total_ic += index_of_coincidence(coset)

    return total_ic / m

def find_key_length(ciphertext: str, max_m: int = 16, language: str = "en") -> int:

    # English random noice IC ~ 0.038
    # Reference text IC ~ 0.063

    threshold = 0.055
    for m in range(1, max_m +1):
        avg_ic = coset_ic(ciphertext, m)

        if avg_ic > threshold:
            return m

    # If none are higher than the threshold, we choose the one
    # with the highest IC
    best_m = 1
    max_ic = 0
    for m in range(1, max_m +1):
        avg_ic = coset_ic(ciphertext, m)
        if avg_ic > max_ic:
            max_ic = avg_ic
            best_m = m

    return best_m

if __name__ == "__main__":

    plaintext = reference_en[0:600]
    ciphertext = vigenere_encrypt(plaintext, "LEMON")

    kl = find_key_length(ciphertext)

    print("m  | Coset Average IC | Note")
    print("---|------------------|----------------")

    for m in range(1, 17):
        ic = coset_ic(ciphertext, m)

        note = ""
        if  m == kl:
            note = "True Key Length"
        elif kl % m == 0:
            note = "Divisor"
        elif m % kl == 0:
            note = "Multiple"

        print(f"{m:<2} | {ic:.4f}           | {note}")
 
    print(f"\nMost likely key length: {kl}")

