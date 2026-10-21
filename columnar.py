# A2 - Columnar Tranposition

def key_order(keyword: str) -> list[int]:

    order = []
    for i in range(len(keyword)):
        order.append(0)

    position = 1
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
    cols = len(keyword)
    padding = len(plaintext) % cols

    # We add padding if necessary
    if padding != 0:
        missing_chars = cols - padding
        for i in range(missing_chars):
            plaintext += pad


    # Now we create empty strings for each column ["", "", ...]
    # This is where the characters will go 
    columns = []
    for i in range(cols):
        columns.append("")

    # We fill the columns
    current_col = 0
    for character in plaintext:
        columns[current_col] += character
        current_col += 1

        if current_col == cols:
            current_col = 0

    # Now we stablish the order and read the columns in that key order
    order = key_order(keyword) 
    ciphertext = ""

    for rank in range(1, cols + 1):
        for i in range(cols):
            if order[i] == rank:
                ciphertext += columns[i]

    return ciphertext

# print(encrypt("MYSECRETMESSAGE", "CIPHER"))
    # Output: MEACSXEEXYTGSMERSX

def decrypt(ciphertext: str, keyword: str) -> str:
    cols = len(keyword)
    count = len(ciphertext) // cols

    columns = []
    for i in range(cols):
        columns.append("")

    order = key_order(keyword)
    index = 0

    for rank in range(1, cols +1 ):
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

# def encrypt_double(plaintext: str, kw1: str, kw2: str, pad: str = "X") -> str

# def decrypt_double(ciphertext: str, kw1: str, kw2: str) -> str

