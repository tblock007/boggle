# Helper node class for the PrefixTrie
class TrieNode:

    def __init__(self):
        self.valid = False
        self.children = {}


    def insert(self, string):
        if string == '':
            self.valid = True
        else:
            # check whether the next letter has already been seen on this path
            # if not, add a new node before recursively inserting the remainder of the screen
            if string[-1] not in self.children.keys():
                self.children[string[-1]] = TrieNode()
            self.children[string[-1]].insert(string[:-1])


    def isValid(self, string):
        if string == '':
            return self.valid
        else:
            letter = string[-1].lower()
            if letter not in self.children.keys():
                return False
            return self.children[letter].isValid(string[:-1])




# A prefix trie class for storing valid words in a dictionary
# Letters are stored as edges between nodes, so that a word is 
# described by a path from root to a leaf
# Each node stores a valid flag indicating whether the path ending 
# at that node represents a path
class PrefixTrie:

    def __init__(self, wordListFile):

        self.root = TrieNode()

        # insert all words in the specified file
        # note that words are stored backwards in the PrefixTrie
        f = open(wordListFile, 'r')
        words = f.readlines()
        for w in words:
            self.root.insert(w.strip()[::-1])
        


    def check(self, word):
        # note that we need to check the reverse of the word since 
        # they are stored backwards in the PrefixTrie
        return self.root.isValid(word[::-1])

    
