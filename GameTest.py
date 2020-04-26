import json
import unittest
from Analyzer import Analyzer
from Game import Game, GameEncoder, GameProperties
from Grid import Grid
from PrefixTrie import PrefixTrie

class GameTest(unittest.TestCase):

    def setUp(self):
        grid = Grid(5, 5, True)
        valid_words = PrefixTrie("lexicons/prefix_trie_test.txt")
        analyzer = Analyzer(valid_words, "English")
        
        self.game = Game('test', GameProperties(min_letters = 4, minutes = 4), grid, analyzer)
        self.game.add_player("T-block")
        self.game.add_player("O-block")
        self.game.add_player("I-block")

    def test_start_end_transitions(self):
        self.assertEqual(self.game.state, "NEW_GAME")
        self.game.start_round()
        self.assertEqual(self.game.state, "ROUND_IN_PROGRESS")
        self.game.end_round()
        self.assertEqual(self.game.state, "GATHERING_LISTS")

    def test_list_gathering_transition(self):
        self.game.start_round()
        self.game.end_round()
        self.assertEqual(self.game.state, "GATHERING_LISTS")

        self.game.add_player_list("T-block", ["a", "b"])        
        self.assertEqual(self.game.state, "GATHERING_LISTS")
        self.game.add_player_list("I-block", ["b", "c"])        
        self.assertEqual(self.game.state, "GATHERING_LISTS")
        self.game.add_player_list("O-block", ["c", "d"])
        self.assertEqual(self.game.state, "BETWEEN_ROUNDS")

    def test_add_player(self):
        self.game.add_player("J-block")
        self.game.start_round()
        self.game.add_player("Z-block") # Should be blocked by ROUND_IN_PROGRESS
        self.assertTrue(self.game.has_player("J-block"))
        self.assertFalse(self.game.has_player("Z-block"))
        self.assertEqual(self.game.num_players(), 4)
        
    def test_remove_player(self):
        self.assertTrue(self.game.has_player("O-block"))
        self.game.remove_player("O-block")
        self.assertFalse(self.game.has_player("O-block"))
        self.game.start_round()
        self.assertTrue(self.game.has_player("T-block"))
        self.game.remove_player("T-block") # Should occur even if ROUND_IN_PROGRESS
        self.assertFalse(self.game.has_player("T-block"))
        self.assertEqual(self.game.num_players(), 1)

    def test_JSON_encode(self):
        self.game.start_round()
        encoded = json.dumps(self.game, cls = GameEncoder)
        expected_prefix = r'{"gid": "test", "state": "ROUND_IN_PROGRESS",'
        expected_suffix = r'"min_letters": 4, "minutes": 4, "language": "English", "player_scores": {"T-block": 0, "O-block": 0, "I-block": 0}}'
        self.assertTrue(encoded.startswith(expected_prefix))
        self.assertTrue(encoded.endswith(expected_suffix))

    # TODO: Add a "full game" test
    

if __name__ == "__main__": 
    unittest.main()   
    