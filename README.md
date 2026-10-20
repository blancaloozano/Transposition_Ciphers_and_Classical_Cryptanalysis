# Transposition_Ciphers_and_Classical_Cryptanalysis

This project forms part of the subject Cryptography for Bachelor in Data Science and Engineering, CEU San Pablo University 26/27. It mathematically implements classic substitution ciphers (Caesars, Affine, Monoalphabetic and Vigenère) alongside automated cryptoanalysis tools. The foundation relies on the chi-squared statisic, comparing the frequency distribution of raw decrypted texts against theoretical English and Spanish language tables. 

The objective is to demonstrate how statisctical analysis breaks algorithms that preserve the underlying language structure, highlighting the practical weakness of simple substitution compared to modern cryptographic systems.

## 1. How to run everything

The program is executed entirely from the terminal by targetting the main executable file, crypto.py. All commands assume you are in the repository root, with Python 3.11+ and no dependencies beyond the standard library (pytest only if you wish to run the automated tests). Here are asome examples on how to run everything:

Part B - The four ciphers
```text
python3 -c "from caesar import encrypt; print(encrypt('MYSECRETMESSAGE', 3))"
python3 -c "from affine import encrypt; print(encrypt('attack', 5,8))"
python3 -c "from monoalpha import encrypt, key_from_keyword; print(encrypt('HELLO', key_from_keyword('CRYPTO')))"
python3 -c "from vigenere import encrypt; print(encrypt('attackatdawn', 'LEMON'))"
```

Part C - The four breakers & Measurement task
```text
python3 -c "from break_caesar import break_caesar; from caesar import encrypt; print(break_caesar(encrypt('THISISASECRETMESSAGE', 11), 'en'))"
python3 -c "from break_affine import break_affine; from affine import encrypt; print(break_affine(encrypt('THISISASECRETMESSAGE', 7, 3), 'en'))"
python3 -c "from break_vigenere import break_vigenere; from vigenere import encrypt; print(break_vigenere(encrypt('THISISASECRETMESSAGEUSEDFORTESTING', 'LEMON'), 5, 'en'))"
python3 -c "from assist import report; print(report('QATNTYSMHQXJOCYHKATM', 'en'))"
python3 measure.py
```

Part D - Command Line Interface (CLI)
```text
python crypto.py <cipher> <mode> [key arguments] [--in FILE] [--out FILE] [--lang en|es]

# Examples:
python crypto.py caesar encrypt --key 3 --in message.txt
python crypto.py affine decrypt --a 5 --b 8 --in cipher.txt --out plain.txt
...
```

## 2. Key Space for each cipher
* Caesar: There are 26 distinct keys, since its a shift of k positions and only k mod 26 matters.
* Affine: The multiplier a must satisfy gcd(a,26) = 1 to ensure a modular inverse exists for decryption. There are 12 coprime values within the 26 letter alphabet (1, 3, 5, 7, 9, 11, 15, 17, 21, 23 and 25). These shift parameter b can take any of the 26 possible alphabetical positions. Multiplying these independent variables yields a total key space of 12 * 26 = 312 distinct keys. 
* Monoalphabetic substitution: The key is a permutation of the 26 letter alphabet, therefore the keyspace is 26! = 4.0329 x 10^26
* Vigenere: for a fixed key length m, each of the m key positions is independently any of 26 letters, giving 26^m keys. A five letter key has 26^5 = 11881376 possibilities. If the key length is unknown, the total key space is the inifnite sum all over m. The attacker must determine m before anything else.

## 3. Caesaer breaker, measured
(The measurement code is available in `measure.py`)

Method: 200 random fragments of a reference text at each length, each encrypted with a random shift, then broken with break_caesar. Recovery rate is the fraction of trials where the recovered shift matches the encryption key exactly.

Based on the empirical measurements, the normalized text yields the following recovery rates:
```text
Plaintext Length     |      Success Rate
20 characters        |          99.0%
30 characters        |          100.0%
40 characters        |          99.0%
60 characters        |          100.0%
100 characters       |          100.0%
```
The chi-squared statistic relies on the Law of Large Numbers. Because the plaintext is stripped of spaces and fully capitalized, the character distribution aligns so perfectly with the theoretical English language frequencies that the automated attack achieves a flawless 100% success rate, even on fragments as short as 20 characters.

## 4. Affine breaker, measure and compared with C1

The cryptanalysis of the Affine cipher utilizes the exact same chi-squared objective function as the Caesar cipher.
The empirical measurements for the Affine breaker are as follows:

```text
Plaintext Length     |      Recovery Rate
20 characters        |         98.0%
30 characters        |         100.0%
40 characters        |         100.0%
60 characters        |         100.0%
100 characters       |         100.0%
```
The statistical reliability is nearly identical to Caesar. At 20 characters, the recovery rate drops marginally to 98.0%, but from 30 characters onward, it guarantees a 100% recovery rate. The only functional difference is computational: the Caesar loop evaluates 26 candidate keys, whereas the Affine loop evaluates 312 permutations. The expanded key space is processed in milliseconds, offering zero additional practical security against statistical analysis.

## 5. Vigenere breaker, measured
To break the Vigenère cipher, the ciphertext is divided into m independent cosets, and the Caesar chi-squared attack is applied to each. The measurement below targets 100 trials across different text and key lengths. 

```text
Key Length (m)       |   60 chars  |  120 chars  |  200 chars  |  300 chars
m = 3                |     100.0%  |     100.0%  |     100.0%  |     100.0%
m = 5                |      99.0%  |     100.0%  |     100.0%  |     100.0%
m = 7                |       0.0%  |      5.0%   |     100.0%  |     100.0%
```
The governing variable for Vigenère cryptanalysis is the length of the individual cosets, not the total length. If a 60 character text is encrypted with a key of $m = 7$, each coset contains fewer than 9 characters. Because such short cosets lack statistical volume, the overall Vigenère recovery fails completely (0.0%). To reliably break Vigenère automatically, the total ciphertext length must be large enough to populate each coset sufficiently (e.g., reaching a 100% success rate at 200+ characters for $m=7$).

## 6. Frequency assistant, run on the cryptogram
When faced with a short (110 character) unknown cryptogram, fully automated chi-squared attacks and direct frequency alignment (mapping the most common ciphertext letter to 'E') both failed. This occurs because 110 characters are insufficient to prevent statistical noise and rank inversions among mid tier frequencies.

To solve this, `assist.py` was used to generate an advanced frequency report. By extracting repeated strings, the most frequent ciphertext trigram was identified and mapped to "THE" (the most common English trigram). This anchored three distinct letters with absolute certainty. These anchors allowed partial words to form, which were then logically deduced by a human operator, bypassing the limitations of purely mathematical evaluation on noisy texts.

## 7. Why 26! is broken in minutes but AES-128 is not
A generic Monoalphabetic cipher boasts a massive key space of $26! \approx 4.03 \times 10^{26}$, making brute force attacks physically impossible for modern computers. Yet, it can be broken in minutes. This vulnerability exists because substitution ciphers lack diffusion. They map one plaintext character to exactly one ciphertext character, perfectly preserving the statistical fingerprint of the plaintext language.

Modern symmetric algorithms like AES128 operate on fundamentally different principles: Confusion and Diffusion. While AES128 has a key space of $2^{128} \approx 3.4 \times 10^{38}$, its strength lies in the fact that changing a single bit in the plaintext alters approximately 50% of the ciphertext bits. The output is statistically indistinguishable from random noise. Because language frequencies are completely obliterated, chi-squared attacks are entirely useless, forcing attackers to rely on impossible searches.

## 8. Limitations

The cryptoanalysis tools and evaluation metrics deployed in this project operate under certain constraints:
* Language Dependence: The chi-squared attack assumes the attacker knows the underlying language (English or Spanish). If a text is encrypted in an unknown or unsupported language, the theoretical frequency tables will misalign, causing the attack to fail.
* Text Volume: Automated attacks are helpless against extremely short messages (e.g., a 10 character password) due to the lack of statistical data within the individual cosets.
* Vigènere Key Length: The implemented Vigenère attack requires the attacker to supply or guess the key length $m$. If $m$ is completely unknown, it must be deduced first (e.g., using the Index of Coincidence or the Kasiski examination) before chi-squared evaluation can begin.

**AI Assistance & Tooling** 
LLMs (Claude & Gemini) were utilized during the development of this project. They helped me in structuring parts of the code, primarily `measure.py`, which was built to extract statistical metrics for the report's analysis. `assist.py` was also heavily developed and refined with AI assistance to support interactive frequency reporting. The models assisted with debugging, error tracking, bug fixes, and structuring sections of this documentation.