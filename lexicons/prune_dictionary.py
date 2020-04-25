def include(word):
    if word[0].isupper():
        return False
    if '.' in word or '\'' in word or '-' in word:
        return False
    return True

def convertLetter(c):
    if c == 'à' or c == 'á' or c == 'â' or c == 'ä': return 'a'
    if c == 'ç': return 'c'
    if c == 'è' or c == 'é' or c == 'ê' or c == 'ë': return 'e'
    if c == 'ì' or c == 'í' or c == 'î' or c == 'ï': return 'i'
    if c == 'ñ': return 'n'
    if c == 'ò' or c == 'ó' or c == 'ô' or c == 'ö': return 'o'
    if c == 'ù' or c == 'ú' or c == 'û' or c == 'ü': return 'u'
    return c

def convertWord(w):
    return ''.join(convertLetter(c) for c in w)

ifstream = open('french_accents.txt', 'r', encoding='utf-8')
ofstream = open('french.txt', 'w+')

words = set(convertWord(line) for line in ifstream.readlines() if include(line))
for w in sorted(words):
    ofstream.write(w)

ifstream.close()
ofstream.close()
