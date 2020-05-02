import json
from apscheduler.schedulers.background import BackgroundScheduler
from collections import Counter
from datetime import datetime, timedelta
from functools import reduce
from transitions import Machine
from typing import NamedTuple

from GameResults import GameResults, GameResultsEncoder
from PrefixTrie import PrefixTrie
from Analyzer import Analyzer


class GameProperties(NamedTuple):    
    min_letters: int = 4
    minutes: int = 4

class Game:

    states = ['NEW_GAME', 'ROUND_IN_PROGRESS', 'GATHERING_LISTS', 'BETWEEN_ROUNDS']

    def __init__(self, gid, properties, grid, analyzer, send_update_callback, list_request_callback, send_analysis_callback):
        self.gid = gid
        self.properties = properties
        self.grid = grid
        self.analyzer = analyzer
        self.scheduler = BackgroundScheduler()
        self.send_update_callback = send_update_callback
        self.list_request_callback = list_request_callback
        self.send_analysis_callback = send_analysis_callback
        self.player_lists = dict()
        self.player_scores = dict()

        self.machine = Machine(model = self, states = Game.states, initial = 'NEW_GAME')
        self.machine.add_transition('start_round', ['NEW_GAME', 'BETWEEN_ROUNDS'], 'ROUND_IN_PROGRESS')
        self.machine.add_transition('end_round', 'ROUND_IN_PROGRESS', 'GATHERING_LISTS', after = ['schedule_force_analysis'])
        self.machine.add_transition('try_get_results', 'GATHERING_LISTS', 'BETWEEN_ROUNDS', conditions = ['all_lists_received'])
        self.machine.on_enter_ROUND_IN_PROGRESS('reset_board')
        self.machine.on_enter_BETWEEN_ROUNDS('analyze_endgame')

        self.scheduler.start()

    # TODO: Make all of the methods that could be called by server return a response to be sent to all players in the room
    # Add players and such would just be a response that adds SERVER message: x has joined the room! etc.
    def add_player(self, username):
        if self.state == 'ROUND_IN_PROGRESS':
            return False
        if username in self.player_scores.keys():
            return False
        self.player_scores[username] = 0
        self.player_lists[username] = []
        return True

    def remove_player(self, username):
        if username in self.player_scores.keys():
            self.player_lists.pop(username, None)
            self.player_scores.pop(username, None)
            return True
        return False

    def has_player(self, username):
        return username in self.player_scores.keys()

    def num_players(self):
        return len(self.player_scores)

    def add_player_list(self, username, word_list):
        if self.state == 'GATHERING_LISTS':
            if username in self.player_scores.keys():
                if username not in self.player_lists.keys():
                    self.player_lists[username] = word_list
                self.try_get_results()
                return True
        return False

    def scheduled_end_round(self):
        self.end_round()
        self.list_request_callback(self.gid)

    def reset_board(self):
        self.player_lists = dict()
        self.grid.reroll()
        self.scheduler.add_job(self.scheduled_end_round, trigger = "date", next_run_time = datetime.now() + timedelta(0, self.properties.minutes * 60))

    def score(self, word):
        if len(word) <= 4: return 1
        elif len(word) == 5: return 2
        elif len(word) == 6: return 3
        elif len(word) == 7: return 5
        elif len(word) == 8: return 11
        else: return (2 * len(word))

    def analyze_endgame(self):
        response = GameResults()
        self.analyzer.set_grid(self.grid.letters)
        response.set_solution(self.get_all_words())
        struck = self.get_common_words()
        for player, word_list in self.player_lists.items():
            invalid = set(w for w in word_list if (len(w) < self.properties.min_letters or not self.analyzer.check(w)))
            remaining = set(word_list) - invalid
            response.add_result(player, "invalid", sorted(invalid))
            response.add_result(player, "struck", sorted(remaining & struck))
            scored = remaining - struck
            scored_list = sorted(scored)
            response.add_result(player, "scored", scored_list)
            response.add_result(player, "scores", [self.score(w) for w in scored_list])
            round_score = sum(self.score(w) for w in scored_list)
            self.player_scores[player] += round_score
        self.send_analysis_callback(self.gid, response.encode())
        self.send_update_callback(self.gid, None, None)

    def scheduled_force_analysis(self):
        if self.state == 'GATHERING_LISTS':
            for username in self.player_scores.keys():
                if username not in self.player_lists:
                    self.player_lists[username] = []
            self.try_get_results()

    def schedule_force_analysis(self):
        self.send_update_callback(self.gid, "ROUND_END", "End of round!")
        # Wait 5 seconds, then run scheduled_force_analysis to stop waiting for those who have not yet sent lists.
        self.scheduler.add_job(self.scheduled_force_analysis, trigger = "date", next_run_time = datetime.now() + timedelta(0, 5))

    def all_lists_received(self):
        return all((p in self.player_lists.keys()) for p in self.player_scores.keys())
  
    def get_common_words(self):
        # Get counts for each player, and then sum them to obtain counts for all words found.
        counts = reduce((lambda c1, c2: c1 + c2), (map(Counter, self.player_lists.values())))
        return set(w for w, c in counts.items() if c > 1)

    def get_all_words(self):
        all_words = [w for w in self.analyzer.find_all_words() if len(w) >= self.properties.min_letters]
        all_words.sort(key = (lambda x: (-1 * len(x), x)))
        return all_words

    def encode(self):
        encoded = dict()
        encoded["gid"] = self.gid
        encoded["state"] = self.state
        encoded["grid"] = self.grid.letters
        encoded["min_letters"] = self.properties.min_letters
        encoded["minutes"] = self.properties.minutes
        encoded["language"] = self.analyzer.language
        encoded["player_scores"] = self.player_scores
        return encoded

class GameEncoder(json.JSONEncoder):
    def default(self, game):
        if isinstance(game, Game):
            return game.encode()
        return json.JSONEncoder.default(self, game)
