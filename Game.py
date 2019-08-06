import Cubes
from PrefixTrie import PrefixTrie
from WordChecker import WordChecker
import json
from functools import reduce
from collections import Counter


class Game:
    def __init__(self, gid, minimumLetters, includeDoubleLetterCube, validWords):
        self.gid = gid
        self.width = 5
        self.height = 5
        self.players = set()
        self.wordLists = dict()
        self.minimumLetters = minimumLetters
        self.includeDoubleLetterCube = includeDoubleLetterCube
        self.checker = WordChecker(validWords)
        self.newRound()

    def __str__(self):
        return '"gid": "{0}", "width": {1}, "height": {2}, "grid": "{3}"'.format(self.gid, self.width, self.height, ','.join(self.grid))

    def newRound(self):
        self.grid = Cubes.getGrid(self.width, self.height, self.includeDoubleLetterCube)
        self.wordLists.clear()
        self.checker.setGrid(self.width, self.height, self.grid)

    def addPlayer(self, user):
        self.players.add(user)

    def removePlayer(self, user):
        if user in self.players:
            self.players.remove(user)

    def allListsSubmitted(self):
        return len(self.players) == len(self.wordLists)

    def setList(self, user, wordList):
        self.wordLists[user] = wordList

    def roundResult(self):
            
        def score(word):
            if len(word) <= 4: return 1
            elif len(word) == 5: return 2
            elif len(word) == 6: return 3
            elif len(word) == 7: return 5
            else: return 11

        counts = reduce((lambda c1, c2: c1 + c2), (map(Counter, self.wordLists.values())))
        struck = set(w for w, c in counts.items() if c > 1)

        results = dict()
        for user in self.wordLists.keys():

            invalid = set(w for w in self.wordLists[user] if (len(w) < self.minimumLetters or not self.checker.check(w)))
            remaining = set(self.wordLists[user]) - invalid
            scored = remaining - struck

            results[user] = dict()            
            results[user]["invalid"] = sorted(invalid)
            results[user]["struck"] = sorted(remaining & struck)
            results[user]["scored"] = sorted(scored)
            results[user]["scores"] = [score(w) for w in results[user]["scored"]]
            results[user]["totalScore"] = sum(results[user]["scores"])

        return json.dumps(results)

    
