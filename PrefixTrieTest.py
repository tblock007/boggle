import unittest
from PrefixTrie import PrefixTrie

class PrefixTrieTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = PrefixTrie("dictionaries/prefix_trie_test.txt")

    def test_presence(self):
        self.assertTrue(self.lexicon.check("banana"))
        self.assertTrue(self.lexicon.check("ban"))
        self.assertTrue(self.lexicon.check("back"))
        self.assertTrue(self.lexicon.check("anana"))
        self.assertFalse(self.lexicon.check("b"))
        self.assertFalse(self.lexicon.check("ba"))
        self.assertFalse(self.lexicon.check("bana"))
        self.assertFalse(self.lexicon.check("banan"))
        self.assertFalse(self.lexicon.check(""))
        self.assertFalse(self.lexicon.check("bananan"))        

if __name__ == "__main__":
    unittest.main()
