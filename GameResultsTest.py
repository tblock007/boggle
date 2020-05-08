import json
import unittest
from GameResults import GameResults, GameResultsEncoder

class GameResultsTest(unittest.TestCase):

    def test_add_improper_result(self):
        results = GameResults()
        with self.assertRaises(Exception):
            results.add_result("T-block", "improper_type", ["a", "b"])

    def test_find_most_unique(self):
        results = GameResults()
        results.add_result("T-block", "invalid", ["abcd", "defg"])
        results.add_result("T-block", "struck", ["can"])
        results.add_result("T-block", "scored", ["orthographic"])
        results.add_result("O-block", "invalid", ["nonword", "notfoundword", "another"])
        results.add_result("O-block", "struck", ["bat", "cat"])
        results.add_result("O-block", "scored", ["orthography", "play", "boggle"])
        results.add_result("J-block", "invalid", [])
        results.add_result("J-block", "struck", ["bat", "cat", "can"])
        results.add_result("J-block", "scored", ["banter"])
        results.compute_most_invalid()
        results.compute_most_struck()
        results.compute_longest_word_found()
        self.assertEqual(results.most_invalid, "O-block")
        self.assertEqual(results.most_struck, "J-block")
        self.assertEqual(results.longest_word, "T-block")

    def test_find_most_non_unique(self):
        results = GameResults()
        results.add_result("T-block", "invalid", ["abcd", "defg", "hijk"])
        results.add_result("T-block", "struck", ["can"])
        results.add_result("T-block", "scored", ["dander"])
        results.add_result("O-block", "invalid", ["nonword", "notfoundword", "another"])
        results.add_result("O-block", "struck", ["bat", "cat", "can"])
        results.add_result("O-block", "scored", ["play", "boggle"])
        results.add_result("J-block", "invalid", [])
        results.add_result("J-block", "struck", ["bat", "cat", "can"])
        results.add_result("J-block", "scored", ["banter"])
        results.compute_most_invalid()
        results.compute_most_struck()
        results.compute_longest_word_found()
        self.assertEqual(results.most_invalid, None)
        self.assertEqual(results.most_struck, None)
        self.assertEqual(results.longest_word, None)

    def test_find_longest_word_with_none_scored(self):
        results = GameResults()
        results.add_result("T-block", "invalid", ["abcd", "defg", "hijk"])
        results.add_result("T-block", "struck", ["can"])
        results.add_result("T-block", "scored", [])
        results.add_result("O-block", "invalid", ["nonword", "notfoundword", "another"])
        results.add_result("O-block", "struck", ["bat", "cat", "can"])
        results.add_result("O-block", "scored", ["boggles"])
        results.add_result("J-block", "invalid", [])
        results.add_result("J-block", "struck", ["bat", "cat", "can"])
        results.add_result("J-block", "scored", ["banter"])
        results.compute_longest_word_found()
        self.assertEqual(results.longest_word, "O-block")

if __name__ == "__main__":
    unittest.main()
