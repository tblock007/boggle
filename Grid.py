import Cubes

# Represents the grid of letters.
class Grid:

    def __init__(self, width, height, includeDoubleLetter):
        self.width = width
        self.height = height
        self.includeDoubleLetter = includeDoubleLetter
        self.letters = [[' ' for _ in range(width)] for _ in range(height)]

    def reroll(self):
        self.letters = Cubes.get_grid(self.width, self.height, self.includeDoubleLetter)