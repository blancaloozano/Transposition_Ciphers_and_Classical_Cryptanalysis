# Transposition Ciphers and Classical Cryptanalysis

This practice forms part of the subject Cryptography for the Bachelor in Data Science and Engineering, CEU San Pablo University 2026/27. It implements classical transposition ciphers (*Rail Fence*, *Columnar Transposition* and *Double Columnar Transposition*), cryptographic measurement tools (*Index of Coincidence*, *Chi-squared Classifier*, *Kasiski Examination*), and automated attacks to break Vigenère and Columnar ciphers without human intervention.

## 1. How to run everything
The program is executed entirely from the terminal by targetting the main executable file, crypto.py.

All commands assume you are in the repository root, with Python 3.11+ and no dependencies beyond the standard library (pytest only if you wish to run the automated tests). Here are some examples on how to run everything:
```text
TO DO 
```


## 2. A3 - Double Transposition & Padding

### Question
*Explain what your `decrypt_double` has to do differently when the plaintext length is not a multiple of both keys, and why a naive implementation returns garbage in that case.*

### Explanation
In a single columnar transposition, when the plaintext length, *N*, is not a multiple of the key length, *K*, padding is added to form a complete matrix. 

In double columnar transposition:
1. **Encryption - Pass 1:** We pad the plaintext to a multiple of $K_1$, producing a text of length $N_1$. 
2. **Encryption - Pass 2:** We take this text of length $N_1$ and pad it to a multiple of $K_2$, producing a final ciphertext of length $N_2$. 

Decryption **unwraps these passes in reverse order.** ($K_2$ first, then $K_1$).

A **naive implementation** fails when $N$ is not a multiple of both key lengths because it attempts to remove padding immediately after decrypting with $K_2$.

If padding is removed right after the $K_2$ decryption pass, the intermediate text length is now below $N_1$ and therefore will fail when running the $K_1$ decryption pass. Columnar transpositions depend strictly on the exact intermediate text length. Altering $N_1$ causes the characters to be extracted incorrectly, outputting the wrong text. `decrypt_double` must preserve the intermediate length $N_1$ between passes and only strip padding after both passes.

Encryption Flow:  

$$\text{Plaintext}_N \xrightarrow[K_1]{\text{pad pass 1}} \text{Intermediate}_{N_1} \xrightarrow[K_2]{\text{pad pass 2}} \text{Ciphertext}_{N_2}$$

Decryption Flow:

$$\text{Ciphertext}_{N_2} \xrightarrow[K_2]{\text{decrypt pass 1}} \text{Intermediate}_{N_1}\xrightarrow[K_1]{\text{decrypt pass 2}} \text{Plaintext}_N$$


## 3. B1 - Index of Coincidence (CRYPTANALYSIS)

### Question
*`CRYPTANALYSIS` is an English word whose index equals that of uniformly random letters. State the shortest text length at which you would trust this measurement, and how you decided.*

### Explanation
The theoretical IC for an English text is $\approx 0.066$ and for uniformly random letters is $\approx \frac{1}{26} = 0.038$.

Short examples usually lack repeating letters purely by chance, producing an IC identical to or lower than random noise. Like we saw with the `CRYPTANALYSIS` example where $N = 13$, it produced an IC of $0.038$

I consider the measurement trustworthy for values of $N = 100$ or higher. To reach this decision I looked at the IC Formula:

$$IC = \frac{\sum{n_L (n_L -1)}}{N (N-1)}$$

where $n_L$ is the count of the letter L in that text and n being the length of the text

Most letter counts are either 0 or 1, either option resulting in a numerator of 0 which artificially pulls the IC towards noise. As $N$ grows, texts are more likely to repeat letters. This forces $n_L \ge 2$, causing positive values to accumulate in the numerator instead of 0s, therefore stabilizing the IC around its theoretical value. I calculated the IC manually for different text lengths, reaching the conclussion that its relibale approximately at $\approx 100$




## 4. B2 - Cipher Classifier

## 5. B3 - Kasiski

TO DO 

## 6. C1 - Coset Index Table

TO DO

## 7. C2 - Vigenère Attack

TO DO 

## 8. C3 - Columnar Transposition Breaker

TO DO 

## 9. Limitations and Observations

The development of this practice helped me see what I did wrong in the previous practice:
* **Missing Experimental Cases**: In P1 I omitted the cross-language comparison tables (such as testing a Spanish text with an English frequency table). In P2, I made sure to fully read all requirements and report complete tables for every requested case.
*  **Qualitative vs. Quantitative Answers**: In P1, I relied too heavily on conceptual descriptions instead of precise numerical findings. In P2, I made sure to provide exact quantitative evidence (like the threshold selection reasoning and better tables)

**AI Assistance** 
LLMs (Claude and Gemini) were used throughout the development of this project. Rather than relying on them to generate the measurement tables or cryptanalysis reports like I wrongly did in P1, they were used to help me understand the code logic, to inspect and fix appearing errors, understand the measurement's task requirements and format the documentation.

All measurements and cipher scripts were executed manually and all report data was independently generated and verified.