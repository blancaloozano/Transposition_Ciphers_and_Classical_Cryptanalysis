def attack(ciphertext: str, n_cols: int, language: str = "en") -> tuple[tuple[int, ...], str]:
    """Returns (column order, plaintext) for a known number of columns."""

    