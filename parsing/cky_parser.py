from collections import defaultdict
from nltk.tree import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        prods = grammar.productions()
        self.start = str(grammar.start())
        self.productions = productions = defaultdict(list)
        for prod in prods:
            act_prod = tuple([str(a) for a in prod.rhs()])
            productions[act_prod].append((str(prod.lhs()), prod.logprob()))
        productions = dict(productions)

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """
        n = len(sent)
        pi = defaultdict(dict)
        bp = defaultdict(dict)
        productions = self.productions

        # init the dicts (if not it doesnt pass tests)
        for i in range(1, n+1):
            for j in range(i, n+1):
                pi[(i, j)]
                bp[(i, j)]

        for i in range(1, n+1):
            act_word = sent[i-1]
            for prod in productions[(act_word, )]:
                pi[(i, i)][prod[0]] = prod[1]
                bp[(i, i)][prod[0]] = Tree(prod[0], [act_word])

        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i+l
                for s in range(i, j):
                    for Y in pi[(i, s)].keys():
                        for Z in pi[(s+1, j)].keys():
                            if (Y, Z) not in productions.keys():
                                continue
                            act_prob = pi[(i, s)][Y] + pi[(s+1, j)][Z]
                            for X in productions[(Y, Z)]:
                                last_prob = pi[(i, j)].get(X[0], float('-inf'))
                                if (last_prob < act_prob + X[1]):
                                    pi[(i, j)][X[0]] = act_prob + X[1]
                                    tree = [bp[(i, s)][Y], bp[(s+1, j)][Z]]
                                    bp[(i, j)][X[0]] = Tree(X[0], tree)

        self._pi = dict(pi)
        self._bp = dict(bp)

        start = self.start
        res = (float("-inf"), Tree(start, sent))  # flatten tree
        if ((1, n) in pi.keys()) & ((1, n) in bp.keys()):
            if (start in pi[(1, n)].keys()) & (start in bp[(1, n)].keys()):
                res = (pi[(1, n)][start], bp[(1, n)][start])
        return(res)
