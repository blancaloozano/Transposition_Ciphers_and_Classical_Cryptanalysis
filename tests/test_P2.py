import unittest

from measure import index_of_coincidence as ic, classify
from kasiski import factor_tally, repeats, distances
from practice1_code.break_caesar import reference_en
import railfence
import columnar

class TestP2(unittest.TestCase):

    def test_railfence_roundtrip(self):
        msg = "DEFENDTHEEASTWALLOFTHECASTLE"
        for rails in [2,3,4,5]:
            ciphertext = railfence.encrypt(msg, rails)
            plaintext = railfence.decrypt(ciphertext, rails)
            self.assertEqual(plaintext, msg)

    def test_columnar_roundtrip(self):
        msg = "WEAREDISCOVEREDSAVEYOURSELF"
        key = "ZEBRAS"
        ciphertext = columnar.encrypt(msg, key)
        plaintext = columnar.decrypt(ciphertext, key)
        self.assertTrue(plaintext.startswith(msg))

    def test_ic_handout_values(self):
        self.assertAlmostEqual(ic("CRYPTANALYSIS"), 0.0385, places=4)
        self.assertAlmostEqual(ic("THEINDEXOFCOINCIDENCE"), 0.0810, places=4)

    def test_kasiski_handout_b3(self):
        text = "ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL ELQYR JXAOA LPKGV D"

        reps = repeats(text, 3)
        self.assertIn("ELQ", reps)

        dists = distances(text, 3)
        self.assertEqual(sorted(list(set(dists))), [15, 35, 50])

        tally = factor_tally(text, 20)
        self.assertIn(5, tally)

    def test_classify_transposition(self):
        msg = (
            "THE INDEX OF COINCIDENCE IS A VERY USEFUL TOOL IN CRYPTANALYSIS "
            "FOR DETERMINING THE TYPE OF CIPHER APPLIED TO A GIVEN CIPHERTEXT "
            "SAMPLE WHEN NO PRIOR INFORMATION IS PROVIDED REGARDING THE ENCRYPTION METHOD "
            "BECAUSE THE FREQUENCY DISTRIBUTION REMAINS UNCHANGED UNDER TRANSPOSITION"
        )
        cipher = columnar.encrypt(msg, "CIPHER")
        self.assertEqual(classify(cipher, language="en"), "transposition")

    def test_edge_cases(self):

        self.assertEqual(ic(""), 0.0)
        self.assertEqual(railfence.encrypt("", 3), "")
        self.assertEqual(columnar.encrypt("", "KEY"), "")

        self.assertEqual(railfence.encrypt("A", 3), "A")

        short_txt = "AB"
        enc_col = columnar.encrypt(short_txt, "KEYWORD")
        self.assertEqual(len(enc_col), 7)

    def test_edge_case_no_letters(self):
        self.assertEqual(ic(""), 0.0)
        self.assertEqual(railfence.encrypt("", 3), "")
        self.assertEqual(columnar.encrypt("", "KEY"), "")
        self.assertEqual(railfence.encrypt("A", 3), "A")
        self.assertEqual(railfence.encrypt("123456789", 3), "")

    def test_ic_b1_specific_texts(self):
        text1 = reference_en[:100]
        text2 = reference_en[:400]
        self.assertAlmostEqual(ic(text1), 0.0634, places = 3)
        self.assertAlmostEqual(ic(text2), 0.0661, places = 3)

if __name__ == "__main__":
    unittest.main()