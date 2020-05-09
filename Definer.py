# A lookup table class that loads in a dictionary (i.e., one that defines
# words) from a text file and provides definition lookups.
class Definer:
    def __init__(self, definitions_file):
        self.lookup = dict()
        with open(definitions_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                word, definition = line.split(None, 1)
                self.lookup[word.lower()] = definition

    # Returns the definition if it is in the dictionary, None otherwise. 
    def define(self, word):
        if word.lower() in self.lookup.keys():
            return self.lookup[word.lower()]
        return None
