import Cubes

# Represents the grid of letters.
class Grid:

    def __init__(self, width, height, includeDoubleLetter):
        self.width = width
        self.height = height
        self.includeDoubleLetter = includeDoubleLetter
        self.letters = None

    def reroll(self):
        self.letters = Cubes.getGrid(self.width, self.height, self.includeDoubleLetter)