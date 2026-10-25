# A2 - Columnar Tranposition

def key_order(keyword: str) -> list[int]:

    clean = []
    for char in keyword.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean.append(char)

    keyword = "".join(clean)


    order = []
    for i in range(len(keyword)):
        order.append(0)

    position = 0
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for letter in alphabet:
        for i in range(len(keyword)):
            if keyword[i] == letter:
                order[i] = position
                position += 1

    return order

# print(key_order("ROTOR"))
    # Output --> [3, 1, 5, 2, 4]

def encrypt(plaintext: str, keyword: str, pad: str = "X") -> str:

    clean_p = []
    for char in plaintext.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean_p.append(char)

    plaintext = "".join(clean_p)

    
    clean_k = []
    for char in keyword.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean_k.append(char)

    keyword = "".join(clean_k)

    cols = len(keyword)
    padding = len(plaintext) % cols

    # We add padding if necessary
    if padding != 0:
        missing_chars = cols - padding
        for i in range(missing_chars):
            plaintext += pad.upper()

    columns = []
    for i in range(cols):
        columns.append("")


    current_col = 0
    for character in plaintext:
        columns[current_col] += character
        current_col += 1

        if current_col == cols:
            current_col = 0

    order = key_order(keyword) 
    ciphertext = ""

    for rank in range(cols):
        for i in range(cols):
            if order[i] == rank:
                ciphertext += columns[i]

    return ciphertext

# print(encrypt("MYSECRETMESSAGE", "CIPHER"))
    # Output: MEACSXEEXYTGSMERSX

def decrypt(ciphertext: str, keyword: str) -> str:

    clean_c = []
    for char in ciphertext.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean_c.append(char)

    ciphertext = "".join(clean_c)
    
    clean_k = []
    for char in keyword.upper():
        char = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U", "Ñ": "N"}.get(char, char)
        if "A" <= char <= "Z":
            clean_k.append(char)

    keyword = "".join(clean_k)
    
    cols = len(keyword)
    count = len(ciphertext) // cols

    columns = []
    for i in range(cols):
        columns.append("")

    order = key_order(keyword)
    index = 0

    for rank in range(cols):
        col = order.index(rank)

        for _ in range(count):
            columns[col] += ciphertext[index]
            index += 1

    plaintext = ""
    for row in range(count):
        for col in columns:
            plaintext += col[row]

    return plaintext

# print(decrypt("MEACSXEEXYTGSMERSX", "CIPHER"))
    # Output: MYSECRETMESSAGEXXX


# A3 - Double Tranposition

def encrypt_double(plaintext: str, kw1: str, kw2: str, pad: str = "X") -> str:

    first_pass = encrypt(plaintext, kw1, pad)
    return encrypt(first_pass, kw2, pad)

# print(encrypt_double("THESAMEKEYMUSTNEVERBEUSEDTWICE", "ROTOR", "ENIGMA"))
    # Output: WCTEIHSTAEVREBEUTMNSUEEDSEEMYK

def decrypt_double(ciphertext: str, kw1: str, kw2: str) -> str:

    first_pass = decrypt(ciphertext, kw2)
    return decrypt(first_pass, kw1)

# print(decrypt_double("WCTEIHSTAEVREBEUTMNSUEEDSEEMYK", "ROTOR", "ENIGMA"))
    # Output: THESAMEKEYMUSTNEVERBEUSEDTWICE
