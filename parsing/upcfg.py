from collections import defaultdict
from nltk.grammar import Nonterminal as N, PCFG, ProbabilisticProduction

from parsing.baselines import Flat
from parsing.cky_parser import CKYParser
from parsing.util import lexicalize, unlexicalize


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        prods = defaultdict(lambda: defaultdict(int))

        p_sents = [p_sent.copy(deep=True) for p_sent in parsed_sents]
        u_p_sents = [unlexicalize(p_sent) for p_sent in p_sents]

        for u_p_sent in u_p_sents:
            u_p_sent.chomsky_normal_form()
            u_p_sent.collapse_unary(collapsePOS=True, collapseRoot=True)

        all_prods = [p_sent.productions() for p_sent in u_p_sents]
        all_prods = [prod for prods in all_prods for prod in prods]

        for prod in all_prods:
            prods[prod.lhs()][prod.rhs()] += 1

        prods = dict(prods)
        prob_prods = []
        for lhs in prods.keys():
            act_lhs = dict(prods[lhs])
            total = sum(act_lhs.values())
            for rhs in act_lhs.keys():
                prob_prods.append(ProbabilisticProduction(
                                        lhs, rhs, prob=act_lhs[rhs] / total))
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
        sent = [tag[0] for tag in tagged_sent]
        prob, tags = self.parser.parse(to_tag)
        start = self.parser.start
        if (prob == float('-inf')):
            # tests require to return the last production
            flat_model = Flat([], start)
            tags = flat_model.parse(tagged_sent)
        tags.un_chomsky_normal_form()
        return(lexicalize(tags, sent))
