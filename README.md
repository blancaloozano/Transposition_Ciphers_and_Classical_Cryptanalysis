# Transposition Ciphers and Classical Cryptanalysis

This practice forms part of the subject Cryptography for the Bachelor in Data Science and Engineering, CEU San Pablo University 2026/27. It implements classical transposition ciphers (*Rail Fence*, *Columnar Transposition* and *Double Columnar Transposition*), cryptographic measurement tools (*Index of Coincidence*, *Chi-squared Classifier*, *Kasiski Examination*), and automated attacks to break Vigenère and Columnar ciphers without human intervention.

## 1. How to run everything
The program is executed entirely from the terminal by targetting the main executable file, ``attack.py``.

All commands assume you are in the repository root, with Python 3.11+ and no dependencies beyond the standard library (pytest only if you wish to run the automated tests). 

How to run tests:
```bash
python -m unittest discover -s tests

python attack.py --in examples/cipher_vigenere.txt --lang en
python attack.py --in examples/cipher_columnar.txt --lang en --cols 5
python attack.py --in examples/cipher_mono.txt --lang en

python measure.py          
python keylength.py       
python break_vigenere.py   
python break_columnar.py  
```

The folder ``/examples`` folder contains three ciphertexts:

```text
File -------------------- Cipher -------------------------- Key -------------------------- Expected Output
cipher_columnar.txt       Columnar Transposition            ROTOR                          TRANSPOSITION
cipher_mono.txt           Monoalphabetic Substitution       QWERTYUIOPASDFGHJKLZXCVBNM	   SUBSTITUTION, MONOALPHABETIC
cipher_vigenere.txt       Vigenère                          LEMON                          SUBSTITUTION, POLYALPHABETIC
```

We also extended ``crypto.py`` from P1. Now, we can also execute the P2 modules directly from that file:

```bash
python crypto.py columnar encrypt --key CIPHER --in examples/message.txt --out examples/cipher.txt
    # DPFENOLSLCNDOONEERIRASGEPRBNIALCYSWSOIIEHDEVNAGTCEAROIOMETEIEOKENKELEIMTIEISSMPSLATUIFERIOR...
python crypto.py columnar decrypt --key CIPHER --in examples/cipher.txt
    # DEVELOPINGEFFECTIVECOMMUNICATIONSKILLSISESSENTIALFORSUCCESSINTHEMODERNPROFESSIONALLANDSCAPE...


python crypto.py railfence encrypt --rails 5 --in examples/message.txt --out examples/cipher.txt
    #EPFIMCNLSIRETDRSLSWEAIAAISNOPSCBITEITCTEOIFOPHECODVYDCRGAHFHDRMILSAEREOAFOROAIIEENEEUTKIELUSERFOAAEY....
python crypto.py railfence decrypt --rails 5 --in examples/cipher.txt
    # DEVELOPINGEFFECTIVECOMMUNICATIONSKILLSISESSENTIALFORSUCCESSINTHEMODERNPROFESSIONALLANDSCAPE...


python crypto.py measure ic --in examples/cipher.txt
    # 0.0661
python crypto.py measure classify --in examples/cipher.txt
    # transposition
python crypto.py measure kasiski --in examples/cipher.txt
    # {2: 11, 3: 5, 4: 7, 5: 2, 6: 3, 7: 1, 8: 5, 9: 2, 10: 1, 11: 3, 12: 2, 13: 1, 14: 1, 15: 1, 16: 3, 17: 0, 18: 1, 19: 0, 20: 0}
```
## 2. A3 - Double Transposition & Padding

### Question
*Explain what your `decrypt_double` has to do differently when the plaintext length is not a multiple of both keys, and why a naive implementation returns garbage in that case.*

### Explanation
In a single columnar transposition, if the plaintext length $N$ is not a multiple of the key length $K$, padding characters are appended to complete the final row so the text forms a perfect rectangular matrix.

In double columnar transposition:
1. **Encryption - Pass 1:** The plaintext is padded to a multiple of $K_1$, producing an intermediate text of length $N_1$. 
2. **Encryption - Pass 2:** The intermediate text of length $N_1$ is padded again to be a multiple of $K_2$, producing a final ciphertext of length $N_2$. 

A **naive implementation** fails for two reasons:
1. **Incorrect order of operations:** A naive approach might try to decrypt using $K_1$ first and then $K_2$. Since encryption applied $K_2$, the matrix geometry and column reordering of $K_2$ are the outermost layer. Decryption **unwraps these passes in reverse order.** ($K_2$ first, then $K_1$).
2. **Matrix geometry and padding misalignment:** When decrypting with $K_2$, the matrix dimensions are based on $N_2$. The intermediate text will contain $N_1$ characters plus the padding during pass 2. If a naive implementation fails to account for this extra padding, the characters will shift position and the $K_1$ decryption matrix will be misaligned, returning garbage text.

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

In order to choose at which length we should trust this measurement, I tested the IC for different lengths [20, 50, 100, 200, 400] in the ``reference_en`` text. Reaching the following:

```text
Length   | IC
-----------------------
20       | 0.0737
50       | 0.0645 <--
100      | 0.0634 <--
200      | 0.0636
400      | 0.0661
```

So, we consider the measurement trustworthy for values of $N = 50-100$ or higher since the IC is $\approx$ 0.066. 

## 4. B2 - Cipher Classifier

### Questions
1. *Choose the threshold yourself, from data. Justify it in the report; do not hard-code a guess*
2. *At which lengths does the classifier work, and at which does it fail?*
3. *Changing only the pad character moves the error rate substantially. Explain the mechanism.* *Compute, for a 66-letter ciphertext containing 6 pad characters, how much the pad alone contributes to the chisquared statistic. Compare that number with your threshold.*
4. *State the design rule this implies for anyone building a cipher that needs padding.*

Measurement Tables:
```text
---------------------- Table 1 Fixed Padding (X) -----------------
Length | Transposition Errors | Substitution Errors | Total Errors
-------------------------------------------------------
60     | 72           | 0            | 24.00%
120    | 30           | 0            | 10.00%
250    | 0            | 0            | 0.00%
400    | 0            | 0            | 0.00%
```

```text
---------------------- Table 2 Random Padding ------------------------
Length | Transposition Errors | Substitution Errors | Total Errors
----------------------------------------------------------------------
60     | 1            | 0            | 0.33%
120    | 0            | 0            | 0.00%
250    | 0            | 0            | 0.00%
400    | 0            | 0            | 0.00%  
```
```text
t    | Transposition errors, X pad | Transposition errors, random pad | Substitution errors
-----------------------------------------------------------------------------------------------
0.5  |                       29.9% |                            23.5% |               0.00%
0.7  |                       15.1% |                             1.4% |               0.00%
1.0  |                       15.1% |                             0.1% |               0.05%
1.5  |                       15.1% |                             0.1% |               0.53%
2.0  |                        5.4% |                             0.0% |               2.55%
3.0  |                        5.4% |                             0.0% |               8.62%
```
### Explanation

#### 1. Threshold Selection

In ``classify`` we perform the chi-square divided by the text length and returns transposition if the score is below a threshold. A transposition keeps the plaintext letter frequencies (low score); a substitution scrambles them (high score).

At first, I treid to take the midpoint of one transposition and one substitution (that depends on the random key: a single substitution scored 13.3 in one run and 2.5 in another), but i quickly realized it was not a good implementation as it misclassified many examples.

Instead, for each length I generated 1500 ciphertexts of each kind with random keys, and swept the threshold t, counting errors over all four lengths

Below $t = 0.7$, short transpositions are misclassified. above $t = 1.5$ substitutions start to be misclassified. So, I decided to choose **$threshold = 1.0$**, the middle point in between them.


#### 2. Lengths for the Classifier to Work

With probabilistic padding the classifier is essentially correct at every tested length. With the fixed ``X`` pad it fails on about 30% of the transpositions for texts below 120, while it never fails for textsa with 120+ characters.

Padding is added to the plaintext before transposing, so the pad letters stay in the ciphertext and change its letter counts. Since ``X`` is one of the rarest english letters, adding it results in an enormous deviation from the english table which is larger the shorter the text- A pad letter drawn from the language distribution deviates much less, which explains why a probabilistic padding obtains much better results.

#### 3. 6-pad Characters in a 66-letter ciphertext

The letter `X` has a frequency of $0.0015$ in the English alphabet. For a ciphertext of length $N = 66$ in english, the expected frequency of `X`is: 

$$E = N * 'X' = 66 * 0.0015 = 0.099$$

if 6 `X` characters are added as padding, the chisquare contribution alone is: 

$$\chi^2_\text{X} = \frac{(O - E)^2}{E} = \frac{(6 - 0.099)^2}{0.099} = \frac{34.8218}{0.099} \approx 351.73$$

Normalizing by the total length:

$$\frac{351.73}{66} \approx 5.329$$

Adding 6 fixed `X` contributes **5.329** to the total chisquare score, **5 times our threshold value of 1.0**, guaranteeing that the ciphertext is going to be misclassified as `substitution` no matter the rest of the letters.

#### 4. Design Rules

We saw that using a fixed, rare character like `X` for padding introduces massive noise. Anyone building a cipher that requires padding must use **probabilistic padding** drawn from the target langauge's letter distribution to prevent this.

## 5. B3 - Kasiski

#### Question
*The greatest common divisor of those three distances is 5, which is the right answer. Explain why your factor_tally must not be replaced by a gcd, and give the condition under which the gcd silently fails.*

#### Explanation

For the handout text, ``repeats`` returns the repeated sequences (``ELQ: [0, 15, 50], ELQY: [0, 50], ...``) and distances gives $15$, $35$ and $50$ (plus $50$ again for each longer sequence that starts at the same place); ``factor_tally(·, 20)`` gives factor 5 the highest count (11), followed by 2 (9) and 10 (9).

If we replaced it with a single Greatest Common Divisor (GCD) calculation across all distances, are considering **accidental coincidences**, which is dangerous. Some short sequences will inevitably repeat by pure statistical chance, completely independent of the key. The GCD will fail (return 1) if there is **at least one accidental repeat** whose distance is coprime (shares no common prime factors) with the true key length.

For example, if the true key length is 5, most distances will be multiples of 5 (15, 35, ...). If a random 3 letter sequence happens to repeat at a distance of 13, the GCD of `(15,35,50,13)` collapses to 1. `factor_tally` ignores this anomaly because 5 will still have massive tally, whereas 13 will only have a tally of 1.

## 6. C1 - Coset Index Table

#### Question
- *. Return the smallest m whose average stands clearly above the baseline, and say in your report what "clearly" means in your code.*
- *Show the full table of coset_ic for m = 1 to 16 on one of your own test ciphertexts, and mark the true key length, its multiples and its divisors*

#### Explanation

In my code, **clearly above the baseline** means ``average coset IC > 0.055:``

We already know uniformly random distribution of letters produce a baseline IC of $\approx 0.038$, while structured English text produces an IC of $\approx 0.066$. The threshold of `0.055` fits between noise and natural language.

In my code, the function evaluates lengths iteratively from 1 to `max_m` and returns the first `m` that crosses this threshold. This prevents the code from returning a multiple of the key length, since multiples also cross the threshold but appear later.

For the table, I used the reference text we've used before, this time only taking the first 600 characters. By using the key "LEMON" I encrypted it reusing `vigenere.py` from practice 1, obtaining the following IC resutls:

```text
m  | Coset Average IC | Note
---|------------------|----------------
1  | 0.0421           | Divisor
2  | 0.0418           | 
3  | 0.0430           | 
4  | 0.0419           | 
5  | 0.0631           | True Key Length
6  | 0.0426           | 
7  | 0.0410           | 
8  | 0.0420           | 
9  | 0.0442           | 
10 | 0.0619           | Multiple
11 | 0.0397           | 
12 | 0.0436           | 
13 | 0.0404           | 
14 | 0.0422           | 
15 | 0.0668           | Multiple
16 | 0.0390           | 

Most likely key length: 5
```
As observed in the table, $m=10$ and $m=15$ (multiples) also produce high IC values, but the function successfully stops at $m=5$ because it is the smallest $m$ crossing the `0.055` threshold.

**Limitation:** A fixed threshold can fail for very short keys: if two key letters are equal or close (e.g. EAA, QEQ), even m = 1 or m = 2 gets an IC above 0.055 and the function returns 1 or 2. This explains why K = 3 never reaches 100% in section 7.

## 7. C2 - Vigenère Attack

#### Questions
1. *The two tables degrade at very different rates. Which quantity governs each?*
2. *Your attack succeeds on a 200-letter ciphertext with a 5-letter key and fails on a 200-letter ciphertext with a 9letter key. Explain why, in terms of the quantity you identified.*
3. *A user of your tool asks how much ciphertext they need. Give them a rule of thumb, as a formula rather than a number*

Measurement tables:

```text
--- Table 1: Complete Key Recovery Rate (%) ---
Length   | K=3    | K=5    | K=7    | K=9   
---------------------------------------------
100      |    75% |    35% |    10% |     2%
150      |    73% |    88% |    27% |    24%
200      |    86% |    9%  |    66% |    73%
300      |    95% |   100% |    70% |    87%
400      |    98% |   100% |   100% |    99%
```

```text
--- Table 2: Key Length Recovery Rate (%) ---
Length   | K=3    | K=5    | K=7    | K=9   
---------------------------------------------
100      |    75% |    81% |    68% |    55%
150      |    73% |    99% |    98% |    83%
200      |    86% |    99% |    97% |    96%
300      |    95% |   100% |    99% |   100%
400      |    98% |   100% |   100% |    99%
```

#### Explanation

**The recovery of the key length (Table 2) is governed by the total length of the ciphertext (N)**. As long as N is large enough for periodic letter allignments to stand out, the Index of Coincidence accross cosets will cross the threshold and identify the key length correctly. 

In contrast, **the recovery of the complete key (Table 1) is governed by the avergage number of caharacters per coset**, given by (N / K). Once the key length is found, the ciphertext is partitioned into K independent Caesar ciphers. Breaking each shift using chi-squared frequency analysis requires sufficient characters within a single coset. If (N / K) is too small, frequency analysis fails, causing the entire key recovery to fail.

For a 200-letter ciphertext with a 5-letter key (K=5), each coset contains N / K = 200 / 5 = 40 characters. A sample size of 40 letters per coset provides enough frequency structure to reliably break the monoalphabetic Caesar shift via chi-squared comparison, yielding a 99% complete key recovery rate.

However, for a 200-letter ciphertext with a 9-letter key (K=9), each coset contains only N / K = 200 / 9 ≈ 22 characters. A sample of 22 letters is statistically noisy for letter frequency distributions, causing the Caesar breaker to pick incorrect shifts in some cosets and dropping the complete key success rate.

To guarantee a reliable key recovery, **each individual coset needs at least 45 to 50 characters** for frequency analysis to work. Therefore, the rule of thumb formula for the required ciphertext length N given a maximum expected key length K is: $$N >= 50 * K$$


## 8. C3 - Columnar Transposition Breaker

#### Question
*n! grows fast. State the largest n your implementation handles in under ten seconds, and describe — without implementing it — one approach that would push that limit further.* 

Measurement table:

```text
--- Table: Columnar Breaker Success Rate (%) ---
Length   | N=4    | N=5    | N=6    | N=7   
---------------------------------------------
60       |   100% |   100% |   100% |   100%
120      |   100% |   100% |   100% |   100%
200      |   100% |   100% |   100% |   100%
```
```text
--- Performance Limit Test ---
Columns (N=7) -> Time: 0.047 seconds
Columns (N=8) -> Time: 0.366 seconds
Columns (N=9) -> Time: 3.229 seconds
Columns (N=10) -> Time: 30.171 seconds
Limit reached! Largest N under 10 seconds is 9.
```

#### Explanation

Single-letter frequencies are completely useless because transposition ciphers only rearrange character positions without altering their identities, meaning **every single one of the n! possible column permutations yields the exact same single-letter frequency distribution**.

My implementation handles up to N = 9 (362,880 permutations) in 3.229 seconds, whereas N = 10 takes 30.171 seconds, hitting the 10-second threshold due to factorial explosion (10! = 3,628,800 permutations).

We could, by evaluating partially reconstructed rows column by column, implement an algorithm that could prune and discard entire branches of permutations as soon as improbable or invalid bigrams/trigrams appear (like stopping immediately when combinations like 'QX' or 'ZX' form, skipping thousands of invalid downstream permutations).

## 9. Pipeline and CLI

``attack.py --in FILE [--lang en|es] [--cols N]`` prints the length, IC and family.
- Transposition → columnar breaker (--cols N required for reliable results).
- Substitution with IC ≥ 0.05 → monoalphabetic (frequency report from P1).
- Substitution with IC < 0.05 → Vigenère: key length, key and plaintext.

**Known limitation.** If ``--cols`` is omitted the program tries the column counts that divide the length and keeps the first, which is not a correct selection criterion (it printed garbage for cipher_columnar.txt). Use --cols. A correct autodetection would score the best candidate of each n with the bigram model and compare per-letter scores across n.

## 10. Limitations and Observations

- All measurements use windows of one text, so plaintexts are not independent.
- The classifier threshold (1.0) is tuned for English; for Spanish (--lang es) it should be re-derived.
- The fixed-threshold key-length rule fails for very short keys with repeated letters (section 6).

The development of this practice helped me see what I did wrong in the previous practice:
* **Missing Experimental Cases**: In P1 I omitted the cross-language comparison tables (such as testing a Spanish text with an English frequency table). In P2, I made sure to fully read all requirements and report complete tables for every requested case.
*  **Qualitative vs. Quantitative Answers**: In P1, I relied too heavily on conceptual descriptions instead of precise numerical findings. In P2, I made sure to provide exact quantitative evidence (like the threshold selection reasoning and better tables)
*  
### Note on ``--cols`` autodetection -- Doesn't work.

When developing ``attack.py``, omitting the ``--cols`` argument was intended to test column counts from 2 to 8 to choose the most appropriate one. However, my code fails to select the optimal solution and always returned a garbage text. **--cols argument is recommended for reliable results** as I couldn't finda  better approach to fix this.

**AI Assistance** 
LLMs (Claude and Gemini) were used throughout the development of this project. Rather than relying on them to generate the cryptanalysis reports like I wrongly did in P1, they were used to help me understand the code logic, inspect and fix appearing errors, clarify measurement task requirements, and generate the unit test suite (`tests/test_P2.py`). Gemini assisted in structuring the measurement benchmarking routines and table-printing logic in `break_columnar.py` and crafting the automated unit tests.

All measurements and cipher scripts were executed manually and all report data was independently generated and verified.
