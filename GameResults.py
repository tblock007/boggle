import json

# Represents the results of a round, including solution and player scores.
class GameResults:

    def __init__(self):
        self.solution = []
        self.scoreboard = dict()
        self.most_invalid = None
        self.most_struck = None
        self.longest_word = None

    def set_solution(self, solved_words):
        self.solution = solved_words

    def add_result(self, player, list_type, values):
        if list_type != "invalid" and list_type != "struck" and list_type != "scored" and list_type != "scores":
            raise Exception("Attempted to add improper list type to GameResults.")
        if player not in self.scoreboard.keys():
            self.scoreboard[player] = dict()
        self.scoreboard[player][list_type] = values

    def find_most(self, list_type):
        counts = {p:len(scoreboard[list_type]) for p, scoreboard in self.scoreboard.items()}
        most_player = max(counts.keys(), key = lambda player: counts[player])
        most_count = counts[most_player]
        if [c for c in counts.values()].count(most_count) == 1:
            return most_player
        return None

    def compute_most_invalid(self):
        self.most_invalid = self.find_most("invalid")

    def compute_most_struck(self):
        self.most_struck = self.find_most("struck")

    def compute_longest_word_found(self):
        lengths = {p:self.length_of_longest_word_found(p) for p in self.scoreboard.keys()}
        most_player = max(lengths.keys(), key = lambda player: lengths[player])
        longest = lengths[most_player]
        if [l for l in lengths.values()].count(longest) == 1:
            self.longest_word = most_player
        else:
            self.longest_word = None

    def length_of_longest_word_found(self, player):
        max_struck = max(self.scoreboard[player]["struck"], key = lambda w: len(w)) if len(self.scoreboard[player]["struck"]) > 0 else ""
        max_scored = max(self.scoreboard[player]["scored"], key = lambda w: len(w)) if len(self.scoreboard[player]["scored"]) > 0 else ""
        return max(len(max_struck), len(max_scored))

    def encode(self):
        result = dict()
        result["scoreboard"] = self.scoreboard
        result["solution"] = self.solution
        result["most_invalid"] = self.most_invalid
        result["most_struck"] = self.most_struck
        result["longest_word"] = self.longest_word
        return result

class GameResultsEncoder(json.JSONEncoder):
    def default(self, results):
        if isinstance(results, GameResults):
            return results.encode()
        return json.JSONEncoder.default(self, obj)
