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
        ['An', 'Er', 'He', 'In', 'Qu', 'Th']] # Bonus cube for 5x5


def getGrid(width, height, includeDoubleLetter):
    if width == 5 and height == 5:
        order = list(range(25))
        if includeDoubleLetter:
            order += [25]
    #elif width == 6 and height == 6:
    #    order = list(range(25, 62))
    else:
        order = list(range(len(cubes)))   
    
    random.shuffle(order)
    return [cubes[order[i]][random.randrange(NFACES)] for i in range(width * height)]
        