import random

NFACES = 6

cubes = [['A', 'A', 'E', 'E', 'E', 'E'], # BEGIN 25 normal cubes of 5x5
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
        ['E', 'N', 'S', 'S', 'S', 'U'], # END 25 normal cubes of 5x5
        ['An', 'Er', 'He', 'In', 'Qu', 'Th'], # Bonus cube for 5x5, BEGIN 36 normal cubes of 6x6
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
        ['E', 'M', 'O', 'T', 'T', 'T']] # END 36 normal cubes of 6x6


def getGrid(width, height, includeDoubleLetter):
    if width == 5 and height == 5:
        order = list(range(25))
        if includeDoubleLetter:
            order += [25]
    elif width == 6 and height == 6:
        order = list(range(25, 61))
    else:
        order = list(range(len(cubes)))   
    
    random.shuffle(order)
    return [cubes[order[i]][random.randrange(NFACES)] for i in range(width * height)]
        