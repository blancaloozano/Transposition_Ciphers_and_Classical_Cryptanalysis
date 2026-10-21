def encrypt(plaintext:str, rails:int) -> str:

    if rails < 2:
        return plaintext

    # Creating the rows (rails) --> ([], [], [], ...)
    rows = []
    for i in range(rails):
        rows.append([])

    rail = 0            # Will tell us the rail we are working on, starting on 0
    down = True         # Will tell us if we go up or down

    for character in plaintext:
        rows[rail].append(character)

        if down:
            rail += 1
        else:
            rail -= 1

        # We stablish the limits
        if rail == 0 or rail == rails - 1:
            down = not down     # If we were going down now we go up and vice versa
        
    ciphertext = ""
    for rail_ in rows:
        for char in rail_:
            ciphertext += char

    return ciphertext


def decrypt(ciphertext: str, rails: int) -> str:

    if rails < 2:
        return ciphertext

    # We need to know how many letters for each rail:
    lengths = []
    for i in range(rails):
        lengths.append(0)

    rail = 0
    down = True

    for i in range(len(ciphertext)):
        lengths[rail] += 1

        if down:
            rail += 1
        else:
            rail -= 1

        if rail == 0 or rail == rails - 1:
            down = not down     # If we were going down now we go up and vice versa

    # Now, we need to "cut" the plaintext to fit the rails
    rows = []
    index = 0

    for length in lengths:
        current_row = []

        for i in range(length):
            current_row.append(ciphertext[index])
            index += 1

        rows.append(current_row)

    # Finally we read the ZigZag using the same logic
    plaintext = ""
    rail = 0
    down = True

    for i in range(len(ciphertext)):
        plaintext += rows[rail].pop(0)

        if down:
            rail += 1
        else:
            rail -= 1

        if rail == 0 or rail == rails - 1:
                    down = not down

    return plaintext

# print(decrypt(encrypt("MYSECRETMESSAGE", 3), 3)) 
    # Output: MYSECRETMESSAGE