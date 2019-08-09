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

            nl = len(self.letters[node])
            if self.letters[node].lower() != string[-1 * nl:].lower():
                return False
            if len(string) == nl:
                return True
            remaining = string[:-1 * nl]

            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    if dfs(neighbor, string[:-1 * nl], [True if i == node else visited[i] for i in range(len(visited))]):
                        return True
            
            return False

        if self.validWords.check(word):
            for i in range(len(self.letters)):
                if dfs(i, word, [False for _ in range(len(self.adjList))]):
                    return True
        return False

    def findAllWords(self):

        def dfsTrieTraverse(node, visited, trieNode):            

            c = self.letters[node].lower()
            if c not in trieNode.children.keys():
                return []

            result = []
            if trieNode.children[c].valid:
                result.append(c)

            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    suffixes = dfsTrieTraverse(neighbor, [True if i == node else visited[i] for i in range(len(visited))], trieNode.children[c])
                    result.extend(map(lambda suffix: c + suffix, suffixes))

            return result


        words = []
        for i in range(len(self.letters)):
            words.extend(dfsTrieTraverse(i, [False for _ in range(len(self.adjList))], self.validWords.root))
        return set(words)

