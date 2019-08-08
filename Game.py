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
        self.playerNames = dict()
        self.minimumLetters = minimumLetters
        self.includeDoubleLetterCube = includeDoubleLetterCube
        self.checker = WordChecker(validWords)
        self.newRound()

    def __str__(self):
        return '"gid": "{0}", "width": {1}, "height": {2}, "grid": "{3}"'.format(self.gid, self.width, self.height, ','.join(self.grid))

    def newRound(self):
        self.grid = Cubes.getGrid(self.width, self.height, self.includeDoubleLetterCube)
        self.checker.setGrid(self.width, self.height, self.grid)

    def addPlayer(self, sid):
        self.players.add(sid)

    def removePlayer(self, sid):
        if sid in self.players:
            self.players.remove(sid)

    def numPlayers(self):
        return len(self.players)

    def resetResults(self):
        self.wordLists.clear()
        self.playerNames.clear()

    def allListsSubmitted(self):
        return len(self.players) == len(self.wordLists)

    def setList(self, sid, username, wordList):
        self.wordLists[sid] = wordList
        self.playerNames[sid] = username

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
        for sid in self.wordLists.keys():

            name = self.playerNames[sid]

            invalid = set(w for w in self.wordLists[sid] if (len(w) < self.minimumLetters or not self.checker.check(w)))
            remaining = set(self.wordLists[sid]) - invalid
            scored = remaining - struck

            results[name] = dict()            
            results[name]["invalid"] = sorted(invalid)
            results[name]["struck"] = sorted(remaining & struck)
            results[name]["scored"] = sorted(scored)
            results[name]["scores"] = [score(w) for w in results[name]["scored"]]
            results[name]["totalScore"] = sum(results[name]["scores"])

        return json.dumps(results)

    
