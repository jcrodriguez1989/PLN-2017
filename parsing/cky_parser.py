from collections import defaultdict
from nltk.tree import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        prods = grammar.productions()
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
                            act_prods = productions[(Y, Z)]
                            act_prob = pi[(i, s)][Y] + pi[(s+1, j)][Z]
                            act_max = (None, float('-inf'))
                            for X in act_prods:
                                if (act_max[1] < act_prob + X[1]):
                                    act_max = (X[0], act_prob + X[1])
                            pi[(i, j)][act_max[0]] = act_max[1]
                            tree = [bp[(i, s)][Y], bp[(s+1, j)][Z]]
                            bp[(i, j)][act_max[0]] = Tree(act_max[0], tree)

        for act_key in pi.keys():
            bp[act_key]  # if not it doesnt pass the tests

        self._pi = dict(pi)
        self._bp = dict(bp)

        res = (float("-inf"), Tree('S', sent))  # flatten tree
        if ((1, n) in pi.keys()) & ((1, n) in bp.keys()):
            if ('S' in pi[(1, n)].keys()) & ('S' in bp[(1, n)].keys()):
                res = (pi[(1, n)]['S'], bp[(1, n)]['S'])
        return(res)
