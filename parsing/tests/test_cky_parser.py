# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log2

from nltk.tree import Tree
from nltk.grammar import PCFG

from parsing.cky_parser import CKYParser


class TestCKYParser(TestCase):

    def test_parse(self):
        grammar = PCFG.fromstring(
            """
                S -> NP VP              [1.0]
                NP -> Det Noun          [0.6]
                NP -> Noun Adj          [0.4]
                VP -> Verb NP           [1.0]
                Det -> 'el'             [1.0]
                Noun -> 'gato'          [0.9]
                Noun -> 'pescado'       [0.1]
                Verb -> 'come'          [1.0]
                Adj -> 'crudo'          [1.0]
            """)

        parser = CKYParser(grammar)

        lp, t = parser.parse('el gato come pescado crudo'.split())

        # check chart
        pi = {
            (1, 1): {'Det': log2(1.0)},
            (2, 2): {'Noun': log2(0.9)},
            (3, 3): {'Verb': log2(1.0)},
            (4, 4): {'Noun': log2(0.1)},
            (5, 5): {'Adj': log2(1.0)},

            (1, 2): {'NP': log2(0.6 * 1.0 * 0.9)},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': log2(0.4 * 0.1 * 1.0)},

            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': log2(1.0) + log2(1.0) + log2(0.4 * 0.1 * 1.0)},

            (1, 4): {},
            (2, 5): {},

            (1, 5): {'S':
                     log2(1.0) +  # rule S -> NP VP
                     log2(0.6 * 1.0 * 0.9) +  # left part
                     log2(1.0) + log2(1.0) + log2(0.4 * 0.1 * 1.0)},  # right part
        }
        self.assertEqualPi(parser._pi, pi)

        # check partial results
        bp = {
            (1, 1): {'Det': Tree.fromstring("(Det el)")},
            (2, 2): {'Noun': Tree.fromstring("(Noun gato)")},
            (3, 3): {'Verb': Tree.fromstring("(Verb come)")},
            (4, 4): {'Noun': Tree.fromstring("(Noun pescado)")},
            (5, 5): {'Adj': Tree.fromstring("(Adj crudo)")},

            (1, 2): {'NP': Tree.fromstring("(NP (Det el) (Noun gato))")},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': Tree.fromstring("(NP (Noun pescado) (Adj crudo))")},

            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': Tree.fromstring(
                "(VP (Verb come) (NP (Noun pescado) (Adj crudo)))")},

            (1, 4): {},
            (2, 5): {},

            (1, 5): {'S': Tree.fromstring(
                """(S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                   )
                """)},
        }
        self.assertEqual(parser._bp, bp)

        # check tree
        t2 = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)
        self.assertEqual(t, t2)

        # check log probability
        lp2 = log2(1.0 * 0.6 * 1.0 * 0.9 * 1.0 * 1.0 * 0.4 * 0.1 * 1.0)
        self.assertAlmostEqual(lp, lp2)

    def test_ambiguous(self):
        #t2 = Tree.fromstring(
        #"""
            #(S
                #(NP (
                    #(NP (Noun dogs))
                    #(PP (
                        #(Prep in)
                        #(NP (Noun houses))
                    #))
                #))
                #(Conj and)
                #(NP (Noun cats))
            #)
        #""")
        #t2.chomsky_normal_form()
        #t2.collapse_unary(collapsePOS=True, collapseRoot=True)

        #t1 = Tree.fromstring(
        #"""
            #(S
                #(NP (Noun dogs))
                #(PP (
                    #(Prep in)
                    #(NP (
                        #(NP (Noun houses))
                        #(Conj and)
                        #(NP (Noun cats))
                    #))
                #))
            #)
        #""")
        #t1.chomsky_normal_form()
        #t1.collapse_unary(collapsePOS=True, collapseRoot=True)
        #t1.draw()

        grammar = PCFG.fromstring(
            """
                S -> NPp Sb<Conj-NP>        [0.8]
                S -> NPpNoun PPp            [0.2]
                NPp -> NPpNoun PPp          [0.5]
                NPp -> NPpNoun b<Conj-NP>   [0.5]
                PPp -> Prep NPpNoun         [0.5]
                PPp -> Prep NPp             [0.5]
                Sb<Conj-NP> -> Conj NPpNoun [1]
                NPpNoun -> 'dogs'           [0.33]
                NPpNoun -> 'houses'         [0.33]
                NPpNoun -> 'cats'           [0.34]
                Prep -> 'in'                [1]
                b<Conj-NP> -> Conj NPpNoun  [1]
                Conj -> 'and'               [1]
            """)

        parser = CKYParser(grammar)

        lp, t = parser.parse('dogs in houses and cats'.split())

        # check chart
        pi = {
            (1, 1): {'NPpNoun': -1.5994620704162712},
            (2, 2): {'Prep': 0.0},
            (3, 3): {'NPpNoun': -1.5994620704162712},
            (4, 4): {'Conj': 0.0},
            (5, 5): {'NPpNoun': -1.556393348524385},

            (1, 2): {},
            (2, 3): {'PPp': -2.599462070416271},
            (3, 4): {},
            (4, 5): {'b<Conj-NP>': -1.556393348524385, 'Sb<Conj-NP>': -1.556393348524385},

            (1, 3): {'S': -6.520852235719904, 'NPp': -5.198924140832542},
            (2, 4): {},
            (3, 5): {'NPp': -4.155855418940656},

            (1, 4): {},
            (2, 5): {'PPp': -5.155855418940656},

            (1, 5): {'S': -7.07724558424429, 'NPp': -7.755317489356927}
        }
        self.assertEqualPi(parser._pi, pi)

        # check partial results
        bp = {
            (1, 1): {'NPpNoun': Tree('NPpNoun', ['dogs'])},
            (2, 2): {'Prep': Tree('Prep', ['in'])},
            (3, 3): {'NPpNoun': Tree('NPpNoun', ['houses'])},
            (4, 4): {'Conj': Tree('Conj', ['and'])},
            (5, 5): {'NPpNoun': Tree('NPpNoun', ['cats'])},

            (1, 2): {},
            (2, 3): {'PPp': Tree('PPp', [Tree('Prep', ['in']), Tree('NPpNoun', ['houses'])])},
            (3, 4): {},
            (4, 5): {'b<Conj-NP>': Tree('b<Conj-NP>', [Tree('Conj', ['and']), Tree('NPpNoun', ['cats'])]), 'Sb<Conj-NP>': Tree('Sb<Conj-NP>', [Tree('Conj', ['and']), Tree('NPpNoun', ['cats'])])},

            (1, 3): {'S': Tree('S', [Tree('NPpNoun', ['dogs']), Tree('PPp', [Tree('Prep', ['in']), Tree('NPpNoun', ['houses'])])]), 'NPp': Tree('NPp', [Tree('NPpNoun', ['dogs']), Tree('PPp', [Tree('Prep', ['in']), Tree('NPpNoun', ['houses'])])])},
            (2, 4): {},
            (3, 5): {'NPp': Tree('NPp', [Tree('NPpNoun', ['houses']), Tree('b<Conj-NP>', [Tree('Conj', ['and']), Tree('NPpNoun', ['cats'])])])},

            (1, 4): {},
            (2, 5): {'PPp': Tree('PPp', [Tree('Prep', ['in']), Tree('NPp', [Tree('NPpNoun', ['houses']), Tree('b<Conj-NP>', [Tree('Conj', ['and']), Tree('NPpNoun', ['cats'])])])])},

            (1, 5): {'S': Tree('S', [Tree('NPp', [Tree('NPpNoun', ['dogs']), Tree('PPp', [Tree('Prep', ['in']), Tree('NPpNoun', ['houses'])])]), Tree('Sb<Conj-NP>', [Tree('Conj', ['and']), Tree('NPpNoun', ['cats'])])]), 'NPp': Tree('NPp', [Tree('NPpNoun', ['dogs']), Tree('PPp', [Tree('Prep', ['in']), Tree('NPp', [Tree('NPpNoun', ['houses']), Tree('b<Conj-NP>', [Tree('Conj', ['and']), Tree('NPpNoun', ['cats'])])])])])}
        }
        self.assertEqual(parser._bp, bp)

        # check log probability
        lp2 = log2(0.8 * 0.5 * 0.33 * 0.5 * 1 * 0.33 * 1 * 1 * 0.34)
        self.assertAlmostEqual(lp, lp2)

    def assertEqualPi(self, pi1, pi2):
        self.assertEqual(set(pi1.keys()), set(pi2.keys()))

        for k in pi1.keys():
            d1, d2 = pi1[k], pi2[k]
            self.assertEqual(d1.keys(), d2.keys(), k)
            for k2 in d1.keys():
                prob1 = d1[k2]
                prob2 = d2[k2]
                self.assertAlmostEqual(prob1, prob2)
