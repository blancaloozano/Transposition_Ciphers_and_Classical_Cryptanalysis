# Transposition Ciphers and Classical Cryptanalysis

This practice forms part of the subject Cryptography for the Bachelor in Data Science and Engineering, CEU San Pablo University 2026/27. It implements classical transposition ciphers (*Rail Fence*, *Columnar Transposition* and *Double Columnar Transposition*), cryptographic measurement tools (*Index of Coincidence*, *Chi-squared Classifier*, *Kasiski Examination*), and automated attacks to break Vigenère and Columnar ciphers without human intervention.

## 1. How to run everything
The program is executed entirely from the terminal by targetting the main executable file, crypto.py.

All commands assume you are in the repository root, with Python 3.11+ and no dependencies beyond the standard library (pytest only if you wish to run the automated tests). Here are some examples on how to run everything:
```text


```


## 2. A3 - Double Transposition & Padding

In a single columnar transposition, when the plaintext length, *N*, is not a multiple of the key length, *K*, padding is added to form a complete matrix. 

In double columnar transposition:
1. **Encryption - Pass 1:** We pad the plaintext to a multiple of $K_1$, producing a text of length $N_1$. 
2. **Encryption - Pass 2:** We take this text of length $N_1$ and pad it to a multiple of $K_2$, producing a final ciphertext of length $N_2$. 

Decryption **unwraps these passes in reverse order.** ($K_2$ first, then $K_1$).

### Why a Naive Implementation Fails

A **naive implementation** fails when $N$ is not a multiple of both key lengths because it attempts to remove padding immediately after decrypting with $K_2$.

If padding is removed right after the $K_2$ decryption pass, the intermediate text length is now below $N_1$ and therefore will fail when running the $K_1$ decryption pass. Columnar transpositions depend strictly on the exact intermediate text length. Altering $N_1$ causes the caharcters to be extracted incorrectly, ouotputting the wrong text. `decrypt_double` must presetve the intermediate length $N_1$ between passes and only strip padding after both passes.

Encryption Flow:  

$$\text{Plaintext}_N \xrightarrow[K_1]{\text{pad pass 1}} \text{Intermediate}_{N_1} \xrightarrow[K_2]{\text{pad pass 2}} \text{Ciphertext}_{N_2}$$

Decryption Flow:

$$\text{Ciphertext}_{N_2} \xrightarrow[K_2]{\text{decrypt pass 1}} \text{Intermediate}_{N_1}!!! \xrightarrow[K_1]{\text{decrypt pass 2}} \text{Plaintext}_N$$


## 3. Index of Coincidence

## 4. Classifier

## 8. Limitations and Observations

The development of this practice helped me see what I did wrong in the previous practice:
* **Missing Experimental Cases**: In P1 I omitted the cross-language comparison tables (such as testing a Spanish text with an English frequency table). In P2, I made sure to fully read all requirements and report complete tables for every requested case.
*  **Qualitative vs. Quantitative Answers**: In P1, I relied too heavily on conceptual descriptions instead of precise numerical findings. In P2, I made sure to provide exact quantitative evidence (like the threshold selection reasoning and better tables)

**AI Assistance** 
LLMs (Claude and Gemini) were used throughout the development of this project. Rather than relying on them to generate the measurement tables or cryptanalysis reports like I wrongly did in P1, they were used to help me understand the code logic, to inspect and fix appearing errors, understand the measurement's task requirements and format the documentation.

All measurements and cipher scripts were executed manually and all report data was independently generated and verified.