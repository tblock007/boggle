import json

# Represents the results of a round, including solution and player scores.
class GameResults:

    def __init__(self):
        self.solution = []
        self.scoreboard = dict()

    def set_solution(self, solved_words):
        self.solution = solved_words

    def add_result(self, player, list_type, values):
        if list_type != "invalid" and list_type != "struck" and list_type != "scored" and list_type != "scores":
            raise Exception("Attempted to add improper list type to GameResults.")
        if player not in self.scoreboard.keys():
            self.scoreboard[player] = dict()
        self.scoreboard[player][list_type] = values

    def encode(self):
        result = dict()
        result["scoreboard"] = self.scoreboard
        result["solution"] = self.solution
        return result

class GameResultsEncoder(json.JSONEncoder):
    def default(self, results):
        if isinstance(results, GameResults):
            return results.encode()
        return json.JSONEncoder.default(self, obj)
