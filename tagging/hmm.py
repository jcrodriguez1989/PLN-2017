from collections import defaultdict
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
        prob = trans.get(prev_tags, dict()).get(tag, 0)
        return prob

    def out_prob(self, word, tag):
        """
        Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        out = self.out
        prob = out.get(tag, dict()).get(word, 0)
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
        self.viterbi_tagger = tagger = ViterbiTagger(self)
        return(tagger.tag(sent))


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm
        self._pi = defaultdict(lambda: defaultdict(tuple))

    def tag(self, sent):
        """
        Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        self._pi = pi = defaultdict(lambda: defaultdict(tuple))
        hmm = self.hmm
        n = hmm.n
        tagset = hmm.tagset
        pi[0][('<s>',)*(n-1)] = (0, [])

        # pi(k,u,v) = max w [ pi(k-1,w,u)*q(v|w,u)*e(xk|v) ]
        for k in range(len(sent)):
            xk = sent[k]  # fixed xk
            pi_k_1 = pi[k]
            pi_k = pi[k+1]
            for prev_tags in pi_k_1.keys():  # fixed w u
                for v in tagset:  # fixed v
                    act_prob = hmm.out_prob(xk, v)
                    if (act_prob == 0):
                        continue
                    act_prob *= hmm.trans_prob(v, prev_tags)
                    if (act_prob == 0):
                        continue
                    act_prob = log(act_prob, 2) + pi_k_1[prev_tags][0]
                    act_tags = pi_k_1[prev_tags][1] + [v]
                    old_prob = pi_k.get(prev_tags[1:] + (v,), float('-inf'))
                    if (old_prob < act_prob):
                        pi_k[prev_tags[1:] + (v,)] = (act_prob, act_tags)
        last_state = list(pi[max(pi.keys())].values())
        last_state.sort(key=lambda x: x[0], reverse=not False)
        return last_state[0][1]


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self.n = n
        self.addone = addone
        self.tcounts = tcounts = defaultdict(int)
        all_words = set()
        self.tagset = tagset = set()
        self.trans = trans = defaultdict(lambda: defaultdict(int))
        self.out = out = defaultdict(lambda: defaultdict(int))

        for sent in tagged_sents:
            tags = [tag[1] for tag in sent]
            words = [word[0] for word in sent]
            all_words = all_words.union(words)
            words = ['<s>']*(n-1) + words + ['</s>']
            tags = ['<s>']*(n-1) + tags + ['</s>']
            for i in range(len(tags) - n+1):
                tagset.add(tags[i])
                out[tags[i]][words[i]] += 1
                ngram = tuple(tags[i:(i+n)])
                tcounts[ngram] += 1  # n grams
                tcounts[ngram[:-1]] += 1  # n-1 grams
        self.all_words = all_words.copy()
        if ('<s>' in tagset):
            tagset.remove('<s>')
        out.pop('<s>', None)
        out.pop('</s>', None)

        # we have counts in out, let's make them probabilities
        for key, val in out.items():
            act_total = sum(val.values())
            for sub_key, sub_val in val.items():
                val[sub_key] = val[sub_key]/act_total

        for ngram in [ngram for ngram in tcounts if len(ngram) == n]:
            #trans[ngram[:-1]][ngram[-1]] = self.tcount(ngram) / self.tcount(ngram[:-1])
            trans[ngram[:-1]][ngram[-1]] = tcounts[ngram] / tcounts[ngram[:-1]]

    def tcount(self, tokens):
        """
        Count for an n-gram or (n-1)-gram of tags.

        tokens -- the n-gram or (n-1)-gram tuple of tags.
        """
        tokens = self.to_tuple(tokens)
        n = self.n
        tokenLen = len(tokens)
        assert (tokenLen == n) | (tokenLen == (n-1))
        actCount = self.tcounts[tokens]
        return actCount

    def unknown(self, w):
        """
        Check if a word is unknown for the model.

        w -- the word.
        """
        return(not w in self.all_words)

    def trans_prob(self, tag, prev_tags):
        """
        Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        addone = self.addone
        trans = self.trans
        if (addone):
            num = self.tcounts(prev_tags + (tag,)) +1 
            denom = self.tcounts(prev_tags) + len(self.tagset) + 1  # for </s>
            prob = num / denom
        else:
            prob = trans.get(prev_tags, dict()).get(tag, 0)
        return prob

    def out_prob(self, word, tag):
        """
        Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        addone = self.addone
        out = self.out
        prob = out.get(tag, dict()).get(word, 0)
        if (addone and self.unknown(word)):
            prob = 1 / len(self.all_words)
        return prob
