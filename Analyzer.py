from PrefixTrie import PrefixTrie

# Responsible for checking whether words are found in the grid, 
# whether they are valid words according to a supplied dictionary,
# and for solving a grid.
class Analyzer:

    def __init__(self, validWords, language):
        self.validWords = validWords
        self.language = language
        
    # TODO: Determine whether neighbor setting is still necessary... can probably just have an implicit graph now
    def set_grid(self, grid):
        # TODO: Rework
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
        # Helper depth-first-search function for traversing the grid. Returns True
        # iff string can be found in the grid starting at node, using only letters
        # that are not yet marked by visited.
        #
        # Note that we actually find words backwards in this function, simply because 
        # it is faster to chop letters off the end of a list rather than the beginning.
        def dfs(node, string, visited):
            # Note we may need to match more than one letter due to the presence of 
            # double letter cubes.
            nl = len(self.letters[node])

            # If we attempt to visit a cube that does not match the next letters of our word,
            # return False immediately.
            if self.letters[node].lower() != string[-1 * nl:].lower():
                return False

            # Oherwise, the cube matches, so if we match the entire string, we can return True.
            if len(string) == nl:
                return True

            # In other cases, we'll need to remove the part that matches this cube and 
            # recursively check the remainder of the string.
            remaining = string[:-1 * nl]

            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    # The recursive call - solve the subproblem starting at the neighboring cube
                    # with a reduced string, updating the visited flags to reflect that we cannot 
                    # revisit this cube.
                    if dfs(neighbor, remaining, [True if i == node else visited[i] for i in range(len(visited))]):
                        return True
            
            # At this point, we have not matched the full string, and we have exhausted 
            # all neighbor choices, so the string is not in the grid.
            return False

        # If the word is in the dictionary, run the dfs from each cube to see if the word is in the grid.
        if self.validWords.check(word):
            for i in range(len(self.letters)):
                if dfs(i, word, [False for _ in range(len(self.adjList))]):
                    return True
        
        # At this point, either the word is not in the dictionary, or it was not found in the grid.
        return False



    def find_all_words(self):
        # Helper depth-first-search function for simultaneously traversing the grid 
        # and the prefix trie. Returns a list of all (sub)strings rooted at trieNode
        # in the prefix trie that can be found in the grid starting at node, using
        # only nodes not yet marked as visited.
        def dfsTrieTraverse(node, visited, trieNode):   
            result = []

            # Check to ensure that including this cube might still be contributing to a valid word.
            # If not (i.e., if it does not exist in the PrefixTrie), we can return an empty list
            # to indicate that taking the cube at node will lead to no valid words.
            # If so, advance down the PrefixTrie to account for these letters and obtain
            # the updated trie node that can be passed to the recursive call.
            c = self.letters[node].lower()
            if len(c) == 1:
                if c not in trieNode.children.keys():
                    return []
                nextNode = trieNode.children[c]
            elif len(c) == 2:  # Handle double letter cubes.
                if c[0] not in trieNode.children.keys():
                    return []
                if c[1] not in trieNode.children[c[0]].children.keys():
                    return []
                nextNode = trieNode.children[c[0]].children[c[1]]

            # If we end up at a valid word, add it to the results.
            if nextNode.valid:
                result.append(c)

            # DFS along the grid by visiting each neighboring cube that has not yet been visited.
            # Construct the result list by appending the current cube to the list returned by the 
            # subproblem recursive call.
            for neighbor in self.adjList[node]:
                if not visited[neighbor]:
                    suffixes = dfsTrieTraverse(neighbor, [True if i == node else visited[i] for i in range(len(visited))], nextNode)
                    result.extend(map(lambda suffix: c + suffix, suffixes))

            return result

        # Accumulate a set of words by starting the DFS traversal from every cube.
        words = []
        for i in range(len(self.letters)):
            words.extend(dfsTrieTraverse(i, [False for _ in range(len(self.adjList))], self.validWords.root))
        return set(words)

