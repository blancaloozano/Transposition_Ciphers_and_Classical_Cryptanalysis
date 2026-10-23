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

where $n_L$ is the count of the letter L in that text and N being the length of the text

In short texts most letter counts are either 0 or 1, contributing nothing to the numerator. With barely any pairs, the numerator cannot accumuate enough matches to reach the theoretical average. Instead, the IC stays trapped in values between 0 and 0.038, acting like random noise.

As $N$ grows, texts are more likely to repeat letters. This forces $n_L \ge 2$, causing positive values to accumulate in the numerator instead of 0s, therefore stabilizing the IC around its theoretical value. I calculated the IC manually for different text lengths, reaching the conclusion that it is reliable at approximately $\approx 100$

## 4. B2 - Cipher Classifier

### Questions
1. *Choose the threshold yourself, from data. Justify it in the report; do not hard-code a guess*
2. *At which lengths does the classifier work, and at which does it fail?*
3. *Changing only the pad character moves the error rate substantially. Explain the mechanism.* *Compute, for a 66-letter ciphertext containing 6 pad characters, how much the pad alone contributes to the chisquared statistic. Compare that number with your threshold.*
4. *State the design rule this implies for anyone building a cipher that needs padding.*

Measurement Tables:
```text
---------------------- Table 1 Fixed Padding (X) ------------------------
Length     |   Transposition Errors  |  Substitution Errors  | Total Errors
60         |     150                 |       0               |     50.0% 
120        |      33                 |       0               |     11.0%  
250        |      0                  |       0               |     0.00% 
400        |      0                  |       0               |     0.00%   
```

```text
---------------------- Table 2 Random Padding ------------------------
Length     |   Transposition Errors  |  Substitution Errors  | Total Errors
60         |     148                 |       0               |     49.3% 
120        |      0                  |       0               |     0.00%  
250        |      0                  |       0               |     0.00% 
400        |      0                  |       0               |     0.00%        
```
### Explanation

#### 1. Threshold Selection

We already know that Transposition changes the position of the letters while Substitution changes the letters themselves. So, for the classifying function I decided to use a threshold of $0.5$ based on how to chi-square scoring function works:
- If a text is close to what we expect (an english text), the chi-score is going to be a near-zero value.
- If a text is not close to what we expect, the chi-score is going to be a really high value 

Therefore, we can assume that a **transposition is going to have a *low* chi-square value** and a **substitution is going to have a *high* chi-square value**. The threshold is chosen to 'protect' the transposition samples from being misclassified as substitutions, but we could have chosen another threshold of 0.6 or 0.7 for example.

#### 2. Lengths for the Classifier to Work

We can see that the classifying function fails for every single one of the 150 columnar transposition samples for a text length of 60, this makes sense since statistically speaking only 60 letters are not enough to classify a text. Adding few more letters to the text (120) improves significantly and adding 250+ ensures that our function is not going to fail. 
- Failure ($N = 60$) $\rightarrow$ The classifier fails for all Transposition Samples for both the fixed and random padding. The sample size is too short.
- Padding Sensitivity ($N = 120$) $\rightarrow$ The classifier fails $11$% of the times under a fixed `X` padding but achieves a $0$% error when using random padding. 
- Success ($N = 250+$) $\rightarrow$ The classifier works for all texts.

#### 3. 6-pad Characters in a 66-letter ciphertext

The letter `X` has a frequency of $0.0015$ in the English alphabet. For a ciphertext of length $N = 66$ in english, the expected frequency of `X`is: 

$$E = N * 'X' = 66 * 0.0015 = 0.099$$

if 6 `X` characters are added as padding, the chisquare contribution alone is: 

$$\chi^2_\text{X} = \frac{(O - E)^2}{E} = \frac{(6 - 0.099)^2}{0.099} = \frac{34.8218}{0.099} \approx 351.73$$

Normalizing by the total length:

$$\frac{351.73}{66} \approx 5.329$$

Adding 6 fixed `X` contributes **5.329** to the total chisquare score, **more than 10 times our threshold value of 0.5**, guaranteeing that the ciphertext is going to be misclassified as `substitution` no matter the rest of the letters.

This also explains why we obtain better error rates for the random padding rather than with a fixed `X` padding, which justifies the design rules explained in the next question.

#### 4. Design Rules

We saw that using a fixed, rare character like `X` for padding introduces massive noise. Anyone building a cipher that requires padding must use **probabilistic padding** drawn from the target langauge's letter distribution to prevent this.

## 5. B3 - Kasiski

#### Question
*The greatest common divisor of those three distances is 5, which is the right answer. Explain why your factor_tally must not be replaced by a gcd, and give the condition under which the gcd silently fails.*

#### Explanation

The `factor_tally` approach highlights the most frequent factors among all distances, which makes it highly robust to noise.

If we replaced it with a single Greatest Common Divisor (GCD) calculation across all distances, are considering **accidental coincidences**, which is dangerous. Some short sequences will inevitably repeat by pure statistical chance, completely independent of the key. The GCD will fail (return 1) if there is **at least one accidental repeat** whose distance is coprime (shares no common prime factors) with the true key length.

For example, if the true key length is 5, most distances will be multiples of 5 (15, 35, ...). If a random 3 letter sequence happens to repeat at a distance of 13, the GCD of `(15,35,50,13)` collapses to 1. `factor_tally` ignores this anomaly because 5 will still have massive tally, whereas 13 will only have a tally of 1.

## 6. C1 - Coset Index Table

#### Question
- *. Return the smallest m whose average stands clearly above the baseline, and say in your report what "clearly" means in your code.*
- *Show the full table of coset_ic for m = 1 to 16 on one of your own test ciphertexts, and mark the true key length, its multiples and its divisors*

#### Explanation

In my code, **clearly above the baseline** means exceeding a fixed threshold of `0.055`.

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

## 7. C2 - Vigenère Attack

#### Question
- *The two tables degrade at very different rates. Which quantity governs each?*
- *Your attack succeeds on a 200-letter ciphertext with a 5-letter key and fails on a 200-letter ciphertext with a 9letter key. Explain why, in terms of the quantity you identified.*
- *A user of your tool asks how much ciphertext they need. Give them a rule of thumb, as a formula rather than a number*

#### Explanation

TO DO

## 8. C3 - Columnar Transposition Breaker

#### Question
n! grows fast. State the largest n your implementation handles in under ten seconds, and describe — without implementing it — one approach that would push that limit further.* 

#### Explanation

TO DO

## 9. Limitations and Observations

The development of this practice helped me see what I did wrong in the previous practice:
* **Missing Experimental Cases**: In P1 I omitted the cross-language comparison tables (such as testing a Spanish text with an English frequency table). In P2, I made sure to fully read all requirements and report complete tables for every requested case.
*  **Qualitative vs. Quantitative Answers**: In P1, I relied too heavily on conceptual descriptions instead of precise numerical findings. In P2, I made sure to provide exact quantitative evidence (like the threshold selection reasoning and better tables)

**AI Assistance** 
LLMs (Claude and Gemini) were used throughout the development of this project. Rather than relying on them to generate the measurement tables or cryptanalysis reports like I wrongly did in P1, they were used to help me understand the code logic, to inspect and fix appearing errors, understand the measurement's task requirements and format the documentation.

All measurements and cipher scripts were executed manually and all report data was independently generated and verified.