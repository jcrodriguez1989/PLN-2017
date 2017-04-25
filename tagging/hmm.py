from math import log

class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.tagset = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """
        Returns the set of tags.
        """
        return self.tagset

    def to_tuple(self, sents):
        """
        Converts list, tuple or string to tuple.

        sents -- the sentence/s to convert
        """
        if isinstance(sents, str):
            res = (sents,)
        elif isinstance(sents, list):
            res = tuple(sents)
        elif isinstance(sents, tuple):
            res = sents
        else:
            res = None
        return res

    def trans_prob(self, tag, prev_tags):
        """
        Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        trans = self.trans
        prob = 0
        if (prev_tags in trans.keys()):
            if (tag in trans[prev_tags].keys()):
                prob = trans[prev_tags][tag]
        return prob

    def out_prob(self, word, tag):
        """
        Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        out = self.out
        prob = 0
        if (tag in out.keys()):
            if (word in out[tag].keys()):
                prob = out[tag][word]
        return prob

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        y -- tagging.
        """
        n = self.n
        y = ['<s>']*(n-1) + y + ['</s>']
        prob = 1
        for i in range(len(y)-n+1):
            prev_tags = self.to_tuple(y[i:i+(n-1)])
            tag = y[i+(n-1)]
            prob *= self.trans_prob(tag, prev_tags)
            if (prob == 0):
                # underflow
                break
        return(prob)

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        prob = self.tag_prob(y)
        for i in range(len(x)):
            act_word = x[i]
            act_tag = y[i]
            prob *= self.out_prob(act_word, act_tag)
            if (prob == 0):
                # underflow
                break
        return(prob)

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        n = self.n
        y = ['<s>']*(n-1) + y + ['</s>']
        prob = 0
        for i in range(len(y)-n+1):
            prev_tags = self.to_tuple(y[i:i+(n-1)])
            tag = y[i+(n-1)]
            actProb = self.trans_prob(tag, prev_tags)
            if (actProb == 0):
                # underflow
                prob = float('-inf')
                break
            prob += log(actProb, 2)
        return(prob)

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
        """
        prob = self.tag_log_prob(y)
        for i in range(len(x)):
            act_word = x[i]
            act_tag = y[i]
            act_prob = self.out_prob(act_word, act_tag)
            if (act_prob == 0):
                # underflow
                prob = float('-inf')
                break
            prob += log(act_prob, 2)
        return(prob)

    def tag(self, sent):
        """
        Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """


class ViterbiTagger:
 
    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
 
    def tag(self, sent):
        """
        Returns the most probable tagging for a sentence.
 
        sent -- the sentence.
        """
