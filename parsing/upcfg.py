from collections import defaultdict
from nltk.grammar import Nonterminal as N, PCFG, ProbabilisticProduction

from parsing.cky_parser import CKYParser
from parsing.util import lexicalize

class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        prods = defaultdict(lambda : defaultdict(int))

        all_prods = [p_sent.productions() for p_sent in parsed_sents]
        all_prods = [prod for prods in all_prods for prod in prods]

        for prod in all_prods:
            prods[prod.lhs()][prod.rhs()] += 1

        prods = dict(prods)
        prob_prods = []
        for lhs in prods.keys():
            act_lhs = dict(prods[lhs])
            total = sum(act_lhs.values())
            for rhs in act_lhs.keys():
                if (len(rhs) == 1):
                    prob_prods.append(ProbabilisticProduction(lhs, [str(lhs)],
                    prob=1))
                    break
                prob_prods.append(ProbabilisticProduction(lhs, rhs,
                    prob=act_lhs[rhs] / total))
        self.prob_prods = prob_prods
        self.parser = CKYParser(PCFG(N(start), prob_prods))

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return(self.prob_prods)

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        to_tag = [tag[1] for tag in tagged_sent]  # wont be used as POS tagger
        _, tags = self.parser.parse(to_tag)
        return(lexicalize(tags, sent))
