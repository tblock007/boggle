import unittest
from Analyzer import Analyzer
from PrefixTrie import PrefixTrie

class AnalyzerTest(unittest.TestCase):
    def setUp(self):
        lexicon = PrefixTrie("lexicons/csw_en.txt")
        self.analyzer = Analyzer(lexicon, "English")

    def test_4x4_solve(self):
        self.analyzer.set_grid([['A', 'T', 'Qu', 'V'],
                                ['R', 'S', 'N', 'I'],
                                ['X', 'I', 'S', 'E'],
                                ['S', 'S', 'L', 'M']])
        solution = self.analyzer.find_all_words()
        expected_words = set(['ar', 'aril', 'arils', 'aris', 'arise', 'arisen', 'ars', 'arsine', 'arsines', 'arsis', 'art', 'arts', 'artsiness', 'as', 'asquint', 'ass', 'assent', 'at', 'ats', 'el', 'elint', 'elints', 'elm', 'elms', 'els', 'elsin', 'elsins', 'em', 'ems', 'en', 'ens', 'entasis', 'entrism', 'ents', 'es', 'ess', 'in', 'inisle', 'inisles', 'ins', 'insist', 'instar', 'intra', 'is', 'isle', 'isles', 'ism', 'issei', 'lei', 'leis', 'lenis', 'lens', 'lent', 'les', 'less', 'li', 'lin', 'line', 'lines', 'lins', 'lint', 'lints', 'lira', 'liras', 'lis', 'list', 'me', 'mein', 'meins', 'meint', 'mel', 'mels', 'men', 'mensa', 'ment', 'menta', 'mes', 'mess', 'ne', 'nelis', 'ness', 'nie', 'nies', 'nil', 'nils', 'nis', 'nisei', 'nisi', 'nisse', 'nix', 'quin', 'quine', 'quines', 'quins', 'quint', 'quinta', 'quintar', 'quintars', 'quintas', 'quints', 'ras', 'rasse', 'rassle', 'rast', 'rat', 'rats', 'rile', 'riles', 'rin', 'rine', 'rines', 'rins', 'rinse', 'rise', 'risen', 'sar', 'sari', 'sarin', 'sarins', 'saris', 'sat', 'sei', 'sel', 'sels', 'sen', 'sens', 'sensa', 'sensi', 'sensis', 'sent', 'sents', 'si', 'sien', 'siens', 'sient', 'sients', 'sile', 'silen', 'sileni', 'silens', 'silent', 'silents', 'siles', 'sin', 'sine', 'sines', 'sins', 'sir', 'sirs', 'sis', 'siss', 'sist', 'sista', 'sistra', 'six', 'snies', 'snirt', 'snirts', 'squint', 'sri', 'sris', 'st', 'star', 'strine', 'strines', 'ta', 'tar', 'tars', 'tarsi', 'tas', 'tass', 'tasse', 'tassel', 'tassels', 'tassie', 'trass', 'trin', 'trine', 'trines', 'trins', 'tsar', 'tsarism', 'vie', 'vies', 'vin', 'vine', 'vines', 'vins', 'vint', 'vints', 'vis', 'vise', 'visile', 'visne', 'xi', 'xis'])
        self.assertEqual(solution, expected_words)

if __name__ == "__main__":
    unittest.main()
