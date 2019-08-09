from PrefixTrie import PrefixTrie

# Responsible for checking whether words are found in the grid, 
# and whether they are valid words according to a supplied dictionary
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

        # helper depth-first-search function for traversing the grid
        # note that we actually find words backwards in this function, simply because 
        # it is faster to chop letters off the end of a list rather than the beginning
        def dfs(node, string, visited): 

            nl = len(self.letters[node])

            # if we attempt to visit a cube that does not match the next letter of our word, return False immediately
            if self.letters[node].lower() != string[-1 * nl:].lower():
                return False

            # otherwise, the cube matches, so if we match the entire string, we can return True
            if len(string) == nl:
                return True

            # in other cases, we'll need to remove the part that matches this cube and recursively check the remainder
            remaining = string[:-1 * nl]

            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    # the recursive call - solve the subproblem starting at the neighboring cube
                    # with a reduced string, updating the visited flags to reflect that we cannot revisit 
                    # this cube
                    if dfs(neighbor, remaining, [True if i == node else visited[i] for i in range(len(visited))]):
                        return True
            
            # at this point, we have not matched the full string, and we have exhausted 
            # all neighbor choices, so the string is not in the grid
            return False

        # if the word is in the dictionary, run the dfs from each cube to see if the word is in the grid
        if self.validWords.check(word):
            for i in range(len(self.letters)):
                if dfs(i, word, [False for _ in range(len(self.adjList))]):
                    return True
        
        # at this point, either the word is not in the dictionary, or it was not found in the grid
        return False



    def findAllWords(self):

        # helper depth-first-search function for simultaneously traversing the grid and the prefix trie
        def dfsTrieTraverse(node, visited, trieNode):            

            result = []

            # check to ensure that including this cube might still be contributing to a valid word
            # if not (i.e., if it does not exist in the PrefixTrie), we can return an empty list
            # if so, advance down the PrefixTrie to account for these letters
            c = self.letters[node].lower()
            if len(c) == 1:
                if c not in trieNode.children.keys():
                    return result
                nextNode = trieNode.children[c]
            elif len(c) == 2:
                if c[0] not in trieNode.children.keys():
                    return result
                if c[1] not in trieNode.children[c[0]].children.keys():
                    return result
                nextNode = trieNode.children[c[0]].children[c[1]]

            # if we end up at a valid word, add it to the results
            if nextNode.valid:
                result.append(c)

            # dfs along the grid by visiting each neighboring cube that has not yet been visited
            # construct the result list by appending the current cube to the list returned by the 
            # subproblem recursive call
            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    suffixes = dfsTrieTraverse(neighbor, [True if i == node else visited[i] for i in range(len(visited))], nextNode)
                    result.extend(map(lambda suffix: c + suffix, suffixes))

            return result

        # accumulate a set of words by starting the dfs traversal from every cube
        words = []
        for i in range(len(self.letters)):
            words.extend(dfsTrieTraverse(i, [False for _ in range(len(self.adjList))], self.validWords.root))
        return set(words)

