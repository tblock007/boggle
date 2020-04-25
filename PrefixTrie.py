# Helper node class for the PrefixTrie.
# The node itself contains a flag indicating whether the path from
# root to the node is a valid word. The node also has a dictionary
# of children, keyed by next letter.
class TrieNode:
    def __init__(self):
        self.valid = False
        self.children = {}

    def insert(self, string):
        if string == '':
            self.valid = True
        else:
            # Check whether the next letter has already been seen on this path.
            # If not, add a new node before recursively inserting the remainder of the string.
            if string[-1] not in self.children.keys():
                self.children[string[-1]] = TrieNode()
            self.children[string[-1]].insert(string[:-1])


    def is_valid(self, string):
        if string == '':
            return self.valid
        else:
            letter = string[-1].lower()
            if letter not in self.children.keys():
                return False
            return self.children[letter].is_valid(string[:-1])




# A prefix trie class for storing valid words in a lexicon.
# Letters are stored as edges between nodes, so that a word is 
# described by a path from the root to some other node.
# Each node stores a valid flag indicating whether the path ending 
# at that node represents a word in the lexicon.
class PrefixTrie:
    def __init__(self, word_list_file):
        self.root = TrieNode()

        # Insert all words in the specified file.
        # Note that words are stored reversed in the PrefixTrie.
        with open(word_list_file, 'r') as f:
            words = f.readlines()
            for w in words:
                self.root.insert(w.strip()[::-1]) 

    # Returns True iff 
    def check(self, word):
        # Note that we need to check the reverse of the word since 
        # they are stored backwards in the PrefixTrie.
        return self.root.is_valid(word[::-1])

    
