from PrefixTrie import PrefixTrie

class WordChecker:
    def __init__(self, validWords):
        self.validWords = validWords
        
    def setGrid(self, width, height, grid):
        self.letters = grid
        self.adjList = [[] for _ in range(width * height)]

        # add left and right neighbors
        for i in range(height):
            for j in range(width - 1):
                index = i * width + j
                self.adjList[index].append(index + 1)
                index = i * width + (j + 1)
                self.adjList[index].append(index - 1)

        # add top and bottom neighbors
        for i in range(height - 1):
            for j in range(width):
                index = i * width + j
                self.adjList[index].append(index + width)
                index = (i + 1) * width + j
                self.adjList[index].append(index - width)

        # add diagonal neighbors
        for i in range(height - 1):
            for j in range(width - 1):
                index = i * width + j
                self.adjList[index].append(index + 1 + width)
                index = i * width + (j + 1)
                self.adjList[index].append(index - 1 + width)
                index = (i + 1) * width + j
                self.adjList[index].append(index + 1 - width)
                index = (i + 1) * width + (j + 1)
                self.adjList[index].append(index - 1 - width)


    def check(self, word):

        def dfs(node, string, visited):
            #print('called with {0} at {1} with visited {2}'.format(string, node, visited))
            if self.letters[node] != string[-1]:
                return False
            if len(string) == 1:
                return True

            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    if dfs(neighbor, string[:-1], [True if i == node else visited[i] for i in range(len(visited))]):
                        return True
            
            return False

        if self.validWords.check(word):
            for i in range(len(self.letters)):
                if dfs(i, word, [False for _ in range(len(self.adjList))]):
                    return True
        return False

