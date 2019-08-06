class TrieNode:
    def __init__(self):
        self.valid = False
        self.children = {}

    def insert(self, string):
        if string == '':
            self.valid = True
        else:
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

class PrefixTrie:

    def __init__(self, wordListFile):

        self.root = TrieNode()

        f = open(wordListFile, 'r')
        words = f.readlines()
        for w in words:
            self.root.insert(w.strip()[::-1])
        
    def check(self, word):
        return self.root.isValid(word[::-1])

    
