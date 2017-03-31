# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import ceil, log
from numpy import cumsum
from random import uniform

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        # it would be nice to have counts for n grams and another for n-1 grams
        # however to facilitate count function, we use just one dict for both
        self.counts = counts = defaultdict(int)
        
        for sent in sents:
            # add n-1 starting and 1 ending markers to each sentence of the
            # corpus
            sent = ['<s>']*(n-1) + sent + ['</s>']
            for i in range(len(sent) -n+1):
                ngram = tuple(sent[i:(i+n)])
                counts[ngram] += 1 # n grams
                counts[ ngram[:-1] ] += 1 # n-1 grams

    def count(self, tokens):
        """
        Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        # if tokens is a word then convert it to tuple (case n=1)
        tokens = tuple(tokens)
        n = self.n
        tokenLen = len(tokens)
        assert (tokenLen == n) | (tokenLen == (n-1))
        actCount = self.counts[tokens]
        return actCount

    def cond_prob(self, token, prev_tokens=None):
        """
        Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n-1

        tokens = prev_tokens + [token]
        prevtokensCount = self.count(prev_tokens)
        # actCondProb will be 0 if prevtokens have probability == 0
        actCondProb = 0
        if (prevtokensCount != 0):
            actCondProb = float(self.count(tokens)) / prevtokensCount
        return actCondProb

    def sent_prob(self, sent):
        """
        Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        n = self.n
        # adding start and end markers to the sentence, as done with corpus
        actSent = ['<s>']*(n-1) + sent + ['</s>']
        sentProb = 1
        for i in range(n-1, len(actSent)):
            actCondProb = self.cond_prob(actSent[i], actSent[(i-n+1):i])
            sentProb *= actCondProb
        return sentProb

    def sent_log_prob(self, sent):
        """
        Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        # well, this code could be used (and passes tests ha), however, to avoid
        # underflow, lets calculate log probability of each gram.
        #sentProb = self.sent_prob(sent)
        ## sentLogProb will be -inf if sentProb == 0
        #sentLogProb = float('-inf')
        #if (sentProb != 0):
            #sentLogProb = log(sentProb, 2)
        #return sentLogProb
        # following, the code to avoid underflow
        n = self.n
        # adding start and end markers to the sentence, as done with corpus
        actSent = ['<s>']*(n-1) + sent + ['</s>']
        sentLogProb = 0
        for i in range(n-1, len(actSent)):
            actCondProb = self.cond_prob(actSent[i], actSent[(i-n+1):i])
            # if the actCondProb == 0 then the total sentLogProb will be -inf
            if (actCondProb == 0):
                sentLogProb = float('-inf')
                break
            actLogCondProb = log(actCondProb, 2)
            sentLogProb += actLogCondProb
        return sentLogProb

class NGramGenerator:
    
    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = n = model.n
        # nexttokenProb is a dict of dict of int, for each prevtokens it will 
        # have the count for each nexttoken from the model
        self.nexttokenProb = nexttokenProb = defaultdict(dict)
        
        counts = model.counts
        for key, val in counts.items():
            # just use the n grams (not n-1)
            if (len(key) == n):
                # here I could use cond_prob, however, as the prevtokens are 
                # the same for each element of my dict, then I cant use the
                # count (saving cpu :P )
                nexttokenProb[ key[:-1] ][ key[-1] ] = val
    
    def generate_sent(self):
        """
        Randomly generate a sentence.
        """
        n = self.n
        retSent = tuple(['<s>']*(n-1))
        prevtokens = retSent
        if (n == 1):
            # with out this, it is very probable that sentences dont start with 
            # the marker
            retSent = ('<s>',)
        acttoken = ""
        while acttoken != '</s>':
            acttoken = self.generate_token(prevtokens)
            prevtokens = (prevtokens + (acttoken,))[1:]
            retSent += (acttoken,)
        return retSent
    
    def generate_token(self, prev_tokens=None):
        """
        Randomly generate a token, given prev_tokens.
    
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        nexttokenProb = self.nexttokenProb
        if not prev_tokens:
            prev_tokens = []
        tokenLen = len(prev_tokens)
        assert (tokenLen == (n-1))
        # get the prob of each possible next token
        nexttokensProb = nexttokenProb[ tuple(prev_tokens) ]
        
        # and the random part of the code
        # example: if nexttokensProb = {'el': 1, 'holiiiiz': 5, 'la': 7}
        # we get a uniform random number between 1-13
        maxRandom = sum(nexttokensProb.values())
        randomNum = ceil(uniform(0, maxRandom))
        acttokens = nexttokensProb.keys()
        # probsSum will have [ 1, 6, 13] so the probability of randomNum to be
        # [0,1] is 1/13, [2,6] is 5/13 and [7,13] is 7/13
        probsSum = cumsum(nexttokensProb.values())
        # so with this we get the index of the last item that makes true
        # i.e. the desired interval
        nexttoken = acttokens[ sum(probsSum < randomNum) ]
        return nexttoken
