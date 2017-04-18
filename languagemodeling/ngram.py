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
            for i in range(len(sent) - n+1):
                ngram = tuple(sent[i:(i+n)])
                counts[ngram] += 1  # n grams
                counts[ngram[:-1]] += 1  # n-1 grams

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

    def log_prob(self, sents):
        """
        Log-probability of sents.

        sents -- the sentences to get (sum) the log-probability.
        """
        logProb = 0
        for sent in sents:
            logProb += self.sent_log_prob(sent)
            if (logProb == float('-inf')):
                break
        return logProb

    def cross_entropy(self, sents):
        """
        Cross-entropy of sents.

        sents -- the sentences to get the cross-entropy.
        """
        # todas las palabras (repetidas)
        m = sum([len(word) for word in sents])
        return self.log_prob(sents) / m

    def perplexity(self, sents):
        """
        Perplexity of sents.

        sents -- the sentences to get the perplexity.
        """
        return 2**(-self.cross_entropy(sents))

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

    #def viterbi(self, sent):
        #"""
        #Find the best segmentation of the sentence.
        #"""
        ## best[i] = best probability for sent[0:i]
        ## words[i] = best word ending at position i
        #n = self.n
        #fsttok = ['<s>']*(n-1)
        #sent = set(sent)
        #sent.add('</s>')
        #actProbs = []
        #fstProb = defaultdict(int)
        #fstProb[tuple(fsttok)] = 1
        #actProbs = [fstProb]

        #actDict = actProbs[-1]
        #for prevtokens in actDict.keys():
            #fstProb.clear()
            #for word in sent:
                #actProb = self.cond_prob(word, list(prevtokens[:(n-1)]))
                #if (actProb != 0):
                    #fstProb[tuple(list(prevtokens) + word)] = actProb * actDict[prevtokens]
            #actProbs.append(fstProb)


        #n = len(sent)
        #words = list(sent)
        #best = [1.0] + [0.0] * n
        #stop = False
        #while !stop:
            
        ### Fill in the vectors best, words via dynamic programming
        #for i in range(n+1):
            #for j in range(0, i):
                #w = sent[j:i]
                #if self.cond_prob(w[-1], w[:-1]) * best[i - len(w)] >= best[i]:
                    #best[i] = self.cond_prob(w) * best[i - len(w)]
                    #words[i] = w
        ### Now recover the sequence of best words
        #sequence = []; i = len(words)-1
        #while i > 0:
            #sequence[0:0] = [words[i]]
            #i = i - len(words[i])
        ### Return sequence of best words and overall probability
        #return sequence, best[-1]


class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        super(AddOneNGram, self).__init__(n, sents)
        # todos los token posibles
        alltokens = set([word for sent in sents for word in sent])
        self.vocabSize = len(alltokens) + 1  # +1 por el </s>

    def V(self):
        """
        Size of the vocabulary.
        """
        return self.vocabSize

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
        prevtokensCount = self.count(prev_tokens) + self.V()
        # actCondProb will be 0 if prevtokens have probability == 0
        actCondProb = 0
        if (prevtokensCount != 0):
            actCondProb = (self.count(tokens)+1.) / prevtokensCount
        return actCondProb


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.gamma = gamma
        if gamma is None:
            # 10% de las sents son para heldOut
            aux = sents[:int(90*len(sents)/100)]
            heldOut = sents[int(90*len(sents)/100):]
            sents = aux
        super(InterpolatedNGram, self).__init__(n, sents)
        # esto lo hago mas que nada para pasar los test. Ya que el modelo para
        # n lo tengo en self.models

        # if addone then the unigram model is AddOne
        if (addone):
            self.models = [AddOneNGram(1, sents)]
        else:
            self.models = [NGram(1, sents)]

        # the rest of the models are NGrams
        for i in range(1, n):
            self.models.append(NGram(i+1, sents))

        # get the best gamma from 1 to 10000, by 100
        if gamma is None:
            self.get_gamma(heldOut, gammaStep=100, maxGamma=10000)

    def get_gamma(self, heldOut, gammaStep=1, maxGamma=20):
        """
        Sets the best gamma, maximizing log_prob.

        heldOut -- sentences to maximize log_prob
        gammaStep -- factor to increment gamma
        maxGamma -- maximum gamma to try
        """
        assert (gammaStep > 0) & (maxGamma > 0)
        maxLogProb = float('-inf')
        self.gamma = 1
        bestGamma = self.gamma
        actLogProb = self.log_prob(heldOut)
        while (maxLogProb < actLogProb) & (self.gamma < maxGamma):
            maxLogProb = actLogProb
            bestGamma = self.gamma
            self.gamma += gammaStep
            actLogProb = self.log_prob(heldOut)
        print("gamma calculated: ", bestGamma, ", with log-prob: ", maxLogProb)
        self.gamma = bestGamma

    def count(self, tokens):
        """
        Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        # if tokens is a word then convert it to tuple (case n=1)
        tokens = tuple(tokens)
        n = self.n
        tokenLen = len(tokens)
        if (tokens == ()):  # to get the unigram model
            tokenLen = 1
        assert (tokenLen == n) | (tokenLen == (n-1))
        actModel = self.models[tokenLen-1]  # n-gram is in position n-1
        actCount = actModel.count(tokens)
        return actCount

    def get_lambdas(self, sent):
        """
        Lambdas for each n-gram.

        sent -- the sentence from which get the lambdas
        """
        gamma = self.gamma
        assert gamma is not None
        models = self.models
        lambdas = []
        sent = tuple(sent)
        for i in range(0, len(sent)-1):
            actSent = sent[i:-1]
            actModel = models[len(actSent)-1]
            actCount = actModel.count(actSent)
            actLambda = actCount/(actCount+gamma)
            actLambda = (1-sum(lambdas))*actLambda
            lambdas.append(actLambda)
        lambdas.append(1-sum(lambdas))  # lambda 1,..,lambda n
        return(lambdas)

    def cond_prob(self, token, prev_tokens=None):
        """
        Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        models = self.models
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n-1

        tokens = prev_tokens + [token]
        lambdas = self.get_lambdas(tokens)
        actCondProb = 0

        for i in range(0, len(tokens)):
            actLambda = lambdas[i]
            acttoken = tokens[i:-1]
            actN = len(acttoken)+1
            actModel = models[actN-1]
            actCondProb += actLambda * actModel.cond_prob(token, acttoken)
        return actCondProb


class BackOffNGram(NGram):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.

        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.beta = beta
        if beta is None:
            # 10% de las sents son para heldOut
            aux = sents[:int(90*len(sents)/100)]
            heldOut = sents[int(90*len(sents)/100):]
            sents = aux
        super(BackOffNGram, self).__init__(n, sents)

        # if addone then the unigram model is AddOne
        if (addone):
            self.models = [AddOneNGram(1, sents)]
        else:
            self.models = [NGram(1, sents)]

        # the rest of the models are NGrams
        for i in range(1, n):
            self.models.append(NGram(i+1, sents))

        # lets create the set for A using 1..n-grams
        self.Acalc = A = defaultdict(set)
        for i in range(2, n+1):
            actModel = self.models[i-1]
            actCounts = actModel.counts
            actIgrams = dict( (k, actCounts[k]) 
                             for k in actCounts if len(k) == i )
            for key in actIgrams.keys():
                actKey = key[:-1]
                actVal = key[-1]
                A[actKey].add(actVal)
                if(actKey == '.'):
                    print(key)

        # get the best beta from 0 to 1, by 0.2
        if beta is None:
            self.get_beta(heldOut, betaStep=0.2, maxbeta=1)

    def get_beta(self, heldOut, betaStep=0.1, maxbeta=1):
        """
        Sets the best beta, maximizing log_prob.

        heldOut -- sentences to maximize log_prob
        betaStep -- factor to increment beta
        maxbeta -- maximum beta to try
        """
        assert (betaStep > 0) & (maxbeta > 0)
        maxLogProb = float('-inf')
        self.beta = 0
        bestbeta = self.beta
        actLogProb = self.log_prob(heldOut)
        while (maxLogProb <= actLogProb) & (self.beta < maxbeta):
            print(bestbeta, maxLogProb, self.beta, actLogProb)  # todo: delete
            maxLogProb = actLogProb
            bestbeta = self.beta
            self.beta += betaStep
            actLogProb = self.log_prob(heldOut)
            print(self.beta, actLogProb)  # todo: delete
        print("beta calculated: ", bestbeta, ", with log-prob: ", maxLogProb)
        self.beta = bestbeta

    def A(self, tokens):
        """
        Set of words with counts > 0 for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        n = self.n
        tokens = self.to_tuple(tokens)
        #assert (0 < len(tokens)) & (len(tokens) < n)
        return self.Acalc[tokens]

    def alpha(self, tokens):
        """
        Missing probability mass for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        n = self.n
        beta = self.beta
        #assert (0 < len(tokens)) & (len(tokens) < n)
        assert beta is not None
        nexttokensCount = len(self.A(tokens))
        alpha = 1
        if (nexttokensCount > 0):
            alpha = beta * nexttokensCount / self.count(tokens)
        return alpha

    def count(self, tokens):
        """
        Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        # if tokens is a word then convert it to tuple (case n=1)
        tokens = self.to_tuple(tokens)
        n = self.n
        tokenLen = len(tokens)

        #assert (tokenLen == n) | (tokenLen == (n-1)) | (tokens == ())

        # para solucionar que no se cuenta el start marker
        if (tokens == tokenLen*('<s>',)):
            tokenLen += 1

        if (tokens == ()):  # to get the unigram model
            tokenLen = 1

        actModel = self.models[tokenLen-1]  # n-gram is in position n-1
        actCount = actModel.count(tokens)
        return actCount

    def count_star(self, tokens):
        """
        Discounted count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        beta = self.beta
        assert beta is not None
        return (self.count(tokens)-beta)

    def denom(self, tokens):
        """
        Normalization factor for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        n = self.n
        #assert (0 < len(tokens)) & (len(tokens) < n)
        followtokens = self.A(tokens)
        tokens = tokens[1:]  # remove x1
        probs = []
        for nexttoken in followtokens:
            actProb = self.cond_prob(nexttoken, tokens)
            #acttokens = self.to_tuple(tokens) + self.to_tuple(nexttoken)
            #actProb = self.count_star(acttokens)
            probs.append(actProb)
        #return (1-(sum(probs) / self.count(tokens)))
        return (1-sum(probs))

    def cond_prob(self, token, prev_tokens=None):
        """
        Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        prev_tokens = self.to_tuple(prev_tokens)

        if not prev_tokens: # i = 1
            # use the unigram model
            return self.models[0].cond_prob(token)
        #assert len(prev_tokens) == n-1

        followtokens = self.A(prev_tokens)
        if token in followtokens:
            acttokens = prev_tokens + self.to_tuple(token)
            actProb = self.count_star(acttokens) / self.count(prev_tokens)
        else:
            actProb = self.cond_prob(token, prev_tokens[1:])
            if (actProb != 0):
                actAlpha = self.alpha(prev_tokens)
                actDenom = self.denom(prev_tokens)
                actProb *= actAlpha/actDenom
        return actProb


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
                nexttokenProb[key[:-1]][key[-1]] = val

    def generate_sent(self):
        """
        Randomly generate a sentence.
        """
        n = self.n
        retSent = tuple(['<s>']*(n-1))
        prevtokens = retSent
        acttoken = ""
        while acttoken != '</s>':
            acttoken = self.generate_token(prevtokens)
            prevtokens = (prevtokens + (acttoken,))[1:]
            retSent += (acttoken,)
        # In test cases I see we should not return starting and ending markers
        # so lets remove them
        retSent = retSent[(n-1):-1]
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
        nexttokensProb = nexttokenProb[tuple(prev_tokens)]

        # and the random part of the code
        # example: if nexttokensProb = {'el': 1, 'holiiiiz': 5, 'la': 7}
        # we get a uniform random number between 1-13
        maxRandom = sum(nexttokensProb.values())
        randomNum = ceil(uniform(0, maxRandom))
        acttokens = list(nexttokensProb.keys())
        # probsSum will have [ 1, 6, 13] so the probability of randomNum to be
        # [0,1] is 1/13, [2,6] is 5/13 and [7,13] is 7/13
        probsSum = cumsum(list(nexttokensProb.values()))
        # so with this we get the index of the last item that makes true
        # i.e. the desired interval
        nexttoken = acttokens[sum(probsSum < randomNum)]
        return nexttoken
        # En R no se usa casi nunca el for.. En que me he convertido!! :'(
