import json
import unittest
from GameResults import GameResults, GameResultsEncoder

class GameResultsTest(unittest.TestCase):

    def test_add_improper_result(self):
        results = GameResults()
        with self.assertRaises(Exception):
            results.add_result("T-block", "improper_type", ["a", "b"])

    def test_JSON_encode(self):
        results = GameResults()
        results.set_solution(["cat", "ban", "bat"])

        results.add_result("T-block", "invalid", ["bal"])
        results.add_result("T-block", "struck", ["bad"])
        results.add_result("T-block", "scored", ["ban", "bat", "cat"])
        results.add_result("T-block", "scores", [1, 1, 1])
        results.add_result("O-block", "invalid", ["bar", "bax"])
        results.add_result("O-block", "struck", ["bad"])
        results.add_result("O-block", "scored", [])
        results.add_result("O-block", "scores", [])

        encoded = json.dumps(results, cls = GameResultsEncoder)        
        expected = r'{"solution": ["ban", "bat", "cat"], "scoreboard": {"T-block": {"invalid": ["bal"], "struck": ["bad"], "scored": ["ban", "bat", "cat"], "scores": [1, 1, 1]}, "O-block": {"invalid": ["bar", "bax"], "struck": ["bad"], "scored": [], "scores": []}}}'
        self.assertEqual(encoded, expected)


if __name__ == "__main__":
    unittest.main()
