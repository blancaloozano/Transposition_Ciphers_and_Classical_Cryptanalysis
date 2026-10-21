# Transposition_Ciphers_and_Classical_Cryptanalysis

This practice forms part of the subject Cryptography for the Bachelor in Data Science and Engineering, CEU San Pablo University 2026/27. It implements classical transposition ciphers (*Rail Fence*, *Columnar Transposition* and *Double Columnar Transposition*), cryptograpihc measurements tools (*Index of Coincidence*, *Chi-squared Classifier*, *Kasiski Examination*), and automated attacks to break Vigenère and Columnar ciphers without human intervention.

This Lab also helped me understand 

## 1. How to run everything
The program is executed entirely from the terminal by targetting the main executable file, crypto.py.

All commands assume you are in the repository root, with Python 3.11+ and no dependencies beyond the standard library (pytest only if you wish to run the automated tests). Here are asome examples on how to run everything:
```text


```


## A3 - Double Transposition & Padding

In a single columnar transposition, when the plaintext length, *N*, is not a multiple of the key length, *K*, padding is added to form a complete matrix. 

In double columnar transposition:
1. **Encryption - Pass 1:** We padd the plaintext to a multiple of *$K_1$*, producing a text of length *$N_1$*. 
2. **Encryption - Pass 2:** We take this text of length *$N_1$* and pad it to a multiple of *$K_2$*, producing a final ciphertext of length *$N_2$*. 

Decryption **unwraps these passes in reverse order.** (*$K_2$* first, then *$K_1$*).

Encryption Flow:  
$$\text{Plaintext}_N \xrightarrow[K_1]{\text{pad pass 1}} \text{Intermediate}_{N_1} \xrightarrow[K_2]{\text{pad pass 2}} \text{Ciphertext}_{N_2}$$

Decryption Flow:
$$\text{Ciphertext}_{N_2} \xrightarrow[K_2]{\text{decrypt pass 1}} \text{Intermediate}_{N_1} \xrightarrow[K_1]{\text{decrypt pass 2}} \text{Plaintext}_N$$

## 3. Index of Coincidence

## 4. Classifier

## 8. Limitations and Observations

The development of this practice helped me see what I did wrong in the previous practice:
* **Missing Experimental Cases**: In P1 I omitted the cross-language comparison tables (such as testing a Spanish text with an English frequency table). In P2, I made sure to fully read all requirements and report complete tables for every requested case.
*  **Qualitative vs. Quantitative Answers**: In P1, I relied to heavily on conceptual descriptions instead of precise numerical findings. In P2, I made sure to provide exact quantitative evidence (like the threshold selection reasoning and better tables)

***AI Assistance** 
LLMS (Claude and Gemini) were used throughout the development of this project. Rather than relying on them to generate the measurement tables or cryptanalysis reports like I wrongly did in P1, they were used to help me understand the code logic, to inspect and fix appearing errors, understand the measurement's task requirements and format the documentation.

All measurements and cipher scripts were executed manually and all report data was independently generated and verified.