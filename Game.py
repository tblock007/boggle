import json
from collections import Counter
from functools import reduce
from transitions import Machine
from typing import NamedTuple

from PrefixTrie import PrefixTrie
from Analyzer import Analyzer

class GameProperties(NamedTuple):    
    minimumLetters: int = 4
    minutes: int = 4

class Game:

    states = ['NEW_GAME', 'ROUND_IN_PROGRESS', 'GATHERING_LISTS', 'BETWEEN_ROUNDS']

    def __init__(self, id, properties, grid, analyzer):
        self.id = id
        self.properties = properties
        self.grid = grid
        self.analyzer = analyzer
        self.players = set()
        self.player_lists = dict()
        self.player_scores = dict()

        self.machine = Machine(model = self, states = Game.states, initial = 'NEW_GAME')
        self.machine.add_transition('start_round', ['NEW_GAME', 'BETWEEN_ROUNDS'], 'ROUND_IN_PROGRESS')
        self.machine.add_transition('end_round', 'ROUND_IN_PROGRESS', 'GATHERING_LISTS')
        self.machine.add_transition('try_get_results', 'GATHERING_LISTS', 'BETWEEN_ROUNDS', conditions = ['all_lists_received'])
        self.machine.on_enter_ROUND_IN_PROGRESS('reset_board')
        self.machine.on_enter_BETWEEN_ROUNDS('analyze_endgame')

    # TODO: Make all of the methods that could be called by server return a response to be sent to all players in the room
    # Add players and such would just be a response that adds SERVER message: x has joined the room! etc.
    def add_player(self, username):
        if self.state == 'ROUND_IN_PROGRESS':
            return False
        self.players.add(username)
        self.player_lists[username] = []
        self.player_scores[username] = 0
        return True

    def remove_player(self, username):
        if username in self.players:
            self.players.remove(username)
            self.player_lists.pop(username, None)
            self.player_scores.pop(username, None)
            return True
        return False

    def add_player_list(self, username, word_list):
        if self.state == 'GATHERING_LISTS':
            if username in self.players:
                self.player_lists[username] = word_list
                self.try_get_results()
                return True
        return False

    # TODO: Rework how the game grid is sent now that it is in 2D
    # TODO: Make it so that __str__ isn't needed
    def __str__(self):
        return '"id": "{0}", "width": {1}, "height": {2}, "grid": [{3}], "minimumLetters": {4}, "minutes": {5}, "language": "{6}"'.format(self.id, self.grid.width, self.grid.height, ','.join(['"{0}"'.format(l) for r in self.grid.letters]), self.properties.minimumLetters, self.properties.minutes, self.analyzer.language)

    def reset_board(self):
        self.player_lists = dict()
        self.grid.reroll()

    def analyze_endgame(self):
        self.analyzer.set_grid(self.grid.letters)
        all_words =self.get_all_words()
        response = {"scoreboard": {}, "solution": all_words}
        struck = self.get_common_words()
        for player, word_list in self.player_lists.items():
            invalid = set(w for w in word_list if (len(w) < self.properties.minimumLetters or not self.analyzer.check(w)))
            remaining = set(word_list) - invalid
            scored = remaining - struck
            response["scoreboard"][player] = dict()            
            response["scoreboard"][player]["invalid"] = sorted(invalid)
            response["scoreboard"][player]["struck"] = sorted(remaining & struck)
            response["scoreboard"][player]["scored"] = sorted(scored)
            response["scoreboard"][player]["scores"] = [self.score(w) for w in response["scoreboard"][player]["scored"]]
            response["scoreboard"][player]["total_score"] = sum(response["scoreboard"][player]["scores"])

        return response

    def all_lists_received(self):
        return all((p in self.player_lists.keys()) for p in self.players)
  
    def get_common_words(self):
        # Get counts for each player, and then sum them to obtain counts for all words found.
        counts = reduce((lambda c1, c2: c1 + c2), (map(Counter, self.player_lists.values())))
        return set(w for w, c in counts.items() if c > 1)

    def get_all_words(self):
        all_words = [w for w in self.analyzer.find_all_words() if len(w) >= self.properties.minimumLetters]
        all_words.sort(key = (lambda x: (-1 * len(x), x)))
        return all_words

    def score(word):
        if len(word) <= 4: return 1
        elif len(word) == 5: return 2
        elif len(word) == 6: return 3
        elif len(word) == 7: return 5
        elif len(word) == 8: return 11
        else: return (2 * len(word))