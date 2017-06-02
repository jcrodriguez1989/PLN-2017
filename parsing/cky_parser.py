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

    #def parse(self, sent):
        #"""Parse a sequence of terminals.

        #sent -- the sequence of terminals.
        #"""
        #n = len(sent)
        #pi = defaultdict(dict)
        #bp = defaultdict(dict)
        #productions = self.productions

        ## init the dicts (if not it doesnt pass tests)
        #for i in range(1, n+1):
            #for j in range(i, n+1):
                #pi[(i, j)]
                #bp[(i, j)]

        #for i in range(1, n+1):
            #act_word = sent[i-1]
            #for prod in productions[(act_word, )]:
                #pi[(i, i)][prod[0]] = prod[1]
                #bp[(i, i)][prod[0]] = Tree(prod[0], [act_word])

        #for l in range(1, n):
            #for i in range(1, n-l+1):
                #j = i+l
                #for s in range(i, j):
                    #for Y in pi[(i, s)].keys():
                        #for Z in pi[(s+1, j)].keys():
                            #if (Y, Z) not in productions.keys():
                                #continue
                            #act_prob = pi[(i, s)][Y] + pi[(s+1, j)][Z]
                            #for X in productions[(Y, Z)]:
                                #last_prob = pi[(i, j)].get(X[0], float('-inf'))
                                #if (last_prob < act_prob + X[1]):
                                    #pi[(i, j)][X[0]] = act_prob + X[1]
                                    #tree = [bp[(i, s)][Y], bp[(s+1, j)][Z]]
                                    #bp[(i, j)][X[0]] = Tree(X[0], tree)

        #self._pi = dict(pi)
        #self._bp = dict(bp)

        #start = self.start
        #res = (float("-inf"), Tree(start, sent))  # flatten tree
        #if ((1, n) in pi.keys()) & ((1, n) in bp.keys()):
            #if (start in pi[(1, n)].keys()) & (start in bp[(1, n)].keys()):
                #res = (pi[(1, n)][start], bp[(1, n)][start])
        #return(res)

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """
        n = len(sent)
        pi = defaultdict(dict)
        bp = defaultdict(dict)
        productions = self.productions

        # init the dicts (if not it doesnt pass tests)
        for i in range(0, n+1):
            for j in range(i, n+1):
                pi[(i, j)]
                bp[(i, j)]

        for i in range(0, n):
            act_word = sent[i]
            for prod in productions[(act_word, )]:
                pi[(i, i+1)][prod[0]] = prod[1]
                bp[(i, i+1)][prod[0]] = Tree(prod[0], [act_word])
            added = True
            while added:
                added = False
                Bs = list(pi[(i, i+1)].keys())
                for B in Bs:
                    for A in productions[(B,)]:  # A is a pair ( A, P(A->B) )
                        prob = A[1] + pi[(i, i+1)][B]
                        if prob > pi[(i, i+1)].get(A[0], float('-inf')):
                            pi[(i, i+1)][A[0]] = prob
                            tree = Tree(B, bp[(i, i+1)][B])
                            bp[(i, i+1)][A[0]] = Tree(A[0], [tree])
                            added = True

        for span in range(2, n+1):
            for begin in range(0, n-span+1):
                end = begin + span
                for split in range(begin+1, end):
                    for B in pi[(begin, split)].keys():
                        for C in pi[(split, end)].keys():
                            if (B, C) not in productions.keys():
                                continue
                            prob = pi[(begin, split)][B] + pi[(split, end)][C]
                            for A in productions[(B, C)]:
                                last_prob = pi[(begin, end)].get(A[0], float('-inf'))
                                if (prob + A[1] > last_prob):
                                    pi[(begin, end)][A[0]] = prob + A[1]
                                    tree = [bp[(begin, split)][B], bp[(split, end)][C]]
                                    bp[(begin, end)][A[0]] = Tree(A[0], tree)
                added = True
                while added:
                    added = False
                    Bs = list(pi[(begin, end)].keys())
                    for B in Bs:
                        for A in productions[(B,)]:  # A is a pair ( A, P(A->B) )
                            prob = A[1] + pi[(begin, end)][B]
                            if prob > pi[(begin, end)].get(A[0], float('-inf')):
                                pi[(begin, end)][A[0]] = prob
                                tree = Tree(B, bp[(begin, end)][B])
                                bp[(begin, end)][A[0]] = Tree(A[0], [tree])
                                added = True

        self._pi = dict(pi)
        self._bp = dict(bp)

        start = self.start
        res = (float("-inf"), Tree(start, sent))  # flatten tree
        if ((0, n) in pi.keys()) & ((0, n) in bp.keys()):
            if (start in pi[(0, n)].keys()) & (start in bp[(0, n)].keys()):
                res = (pi[(0, n)][start], bp[(0, n)][start])
        return(res)
