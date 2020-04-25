def convertLine(l):
    return (l.split()[0] + '\n')

ifstream = open('CSW19defs.txt', 'r', encoding='utf-8')
ofstream = open('csw_en.txt', 'w+')

words = [convertLine(line) for line in ifstream.readlines()[1:]]
for w in words:
    ofstream.write(w)

ifstream.close()
ofstream.close()
