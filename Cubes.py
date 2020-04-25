import random

NFACES = 6

START4X4 = 0
END4X4 = 15
START5X5 = 16
END5X5 = 40
BONUS5X5 = 41
START6X6 = 41
END6X6 = 76
cubes = [['A', 'A', 'E', 'E', 'N', 'G'], # [0] BEGIN 16 normal cubes of 4x4
        ['D', 'E', 'L', 'R', 'V', 'Y'],
        ['E', 'L', 'R', 'T', 'T', 'Y'],
        ['D', 'E', 'I', 'L', 'R', 'X'],
        ['E', 'I', 'O', 'S', 'S', 'T'],
        ['E', 'E', 'G', 'H', 'N', 'W'],
        ['H', 'I', 'M', 'N', 'Qu', 'U'],
        ['H', 'L', 'N', 'N', 'R', 'Z'],
        ['E', 'E', 'I', 'N', 'S', 'U'],
        ['D', 'I', 'S', 'T', 'T', 'Y'],
        ['A', 'O', 'O', 'T', 'T', 'W'],
        ['A', 'C', 'H', 'O', 'P', 'S'],
        ['C', 'I', 'M', 'O', 'T', 'U'],
        ['A', 'B', 'B', 'J', 'O', 'O'],
        ['E', 'H', 'R', 'T', 'V', 'W'],
        ['A', 'F', 'F', 'K', 'P', 'S'], # [15] END 16 normal cubes of 4x4
        ['A', 'A', 'E', 'E', 'E', 'E'], # [16] BEGIN 25 normal cubes of 5x5
        ['E', 'M', 'O', 'T', 'T', 'T'], 
        ['I', 'K', 'L', 'Qu', 'U', 'W'], 
        ['C', 'E', 'I', 'L', 'P', 'T'], 
        ['D', 'D', 'H', 'N', 'O', 'T'], 
        ['A', 'E', 'E', 'E', 'E', 'M'], 
        ['F', 'I', 'P', 'R', 'S', 'Y'], 
        ['D', 'H', 'H', 'L', 'N', 'O'], 
        ['D', 'H', 'H', 'L', 'O', 'R'], 
        ['A', 'D', 'E', 'N', 'N', 'N'],
        ['C', 'C', 'E', 'N', 'S', 'T'],
        ['N', 'O', 'O', 'U', 'T', 'W'],
        ['O', 'O', 'O', 'T', 'U', 'U'],
        ['B', 'J', 'K', 'Qu', 'X', 'Z'],
        ['C', 'E', 'I', 'P', 'S', 'T'],
        ['A', 'F', 'I', 'R', 'S', 'Y'],
        ['E', 'I', 'I', 'T', 'T', 'T'],
        ['A', 'E', 'E', 'G', 'M', 'U'],
        ['G', 'O', 'R', 'R', 'V', 'W'],
        ['C', 'E', 'I', 'I', 'L', 'T'],
        ['A', 'A', 'A', 'F', 'R', 'S'],
        ['A', 'A', 'F', 'I', 'R', 'S'],
        ['A', 'E', 'G', 'M', 'N', 'N'],
        ['D', 'H', 'L', 'N', 'O', 'R'],
        ['E', 'N', 'S', 'S', 'S', 'U'], # [40] END 25 normal cubes of 5x5
        ['An', 'Er', 'He', 'In', 'Qu', 'Th'], # [41] Bonus cube for 5x5, BEGIN 36 normal cubes of 6x6
        ['C', 'E', 'I', 'I', 'T', 'T'],
        ['I', 'P', 'R', 'S', 'Y', 'Y'],
        ['A', 'E', 'G', 'M', 'N', 'N'],
        ['H', 'I', 'R', 'S', 'T', 'V'],
        ['A', 'E', 'I', 'L', 'M', 'N'],
        ['C', 'D', 'D', 'L', 'N', 'N'],
        ['E', 'I', 'L', 'P', 'S', 'T'],
        ['H', 'O', 'P', 'R', 'S', 'T'],
        ['A', 'B', 'D', 'E', 'I', 'O'],
        ['D', 'H', 'L', 'N', 'O', 'R'],
        ['J', 'K', 'Qu', 'W', 'X', 'Z'],
        ['N', 'O', 'O', 'T', 'U', 'W'],
        ['D', 'H', 'H', 'L', 'O', 'R'],
        ['A', 'A', 'E', 'E', 'O', 'O'],
        ['E', 'I', 'O', '.', '.', '.'],
        ['G', 'O', 'R', 'R', 'V', 'W'],
        ['A', 'D', 'E', 'N', 'N', 'N'],
        ['A', 'A', 'E', 'E', 'E', 'E'],
        ['A', 'A', 'A', 'F', 'R', 'S'],
        ['E', 'H', 'I', 'L', 'R', 'S'],
        ['C', 'E', 'I', 'P', 'S', 'T'],
        ['C', 'C', 'E', 'N', 'S', 'T'],
        ['E', 'I', 'I', 'L', 'S', 'T'],
        ['D', 'D', 'H', 'N', 'O', 'T'],
        ['C', 'F', 'G', 'N', 'U', 'Y'],
        ['O', 'O', 'O', 'T', 'T', 'U'],
        ['A', 'F', 'I', 'R', 'S', 'Y'],
        ['A', 'E', 'I', 'N', 'O', 'U'],
        ['D', 'H', 'H', 'N', 'O', 'W'],
        ['A', 'E', 'E', 'G', 'M', 'U'],
        ['B', 'B', 'J', 'K', 'X', 'Z'],
        ['A', 'E', 'E', 'E', 'E', 'M'],
        ['A', 'A', 'F', 'I', 'R', 'S'],
        ['E', 'N', 'S', 'S', 'S', 'U'],
        ['E', 'M', 'O', 'T', 'T', 'T']] # END [76] 36 normal cubes of 6x6


# Generates a random grid of a given width and height.
# 4x4, 5x5, and 6x6 have tailored cubesets. Other sizes
# will draw from all available cubes.
def getGrid(width, height, includeDoubleLetter):
    if width * height > len(cubes):
        raise Exception("Not enough cubes.") 
    if width == 4 and height == 4:
        order = list(range(START4X4, END4X4 + 1))
    elif width == 5 and height == 5:
        order = list(range(START5X5, END5X5 + 1))
        if includeDoubleLetter:
            order += [BONUS5X5]
    elif width == 6 and height == 6:
        order = list(range(START6X6, END6X6 + 1))
    else:
        order = list(range(len(cubes)))   
    
    random.shuffle(order)
    result = [['.' for j in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            index = i * width + j
            result[i][j] = cubes[order[index]][random.randrange(NFACES)]
    return result
        