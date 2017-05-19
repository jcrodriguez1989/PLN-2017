from collections import defaultdict
from featureforge.vectorizer import Vectorizer
from itertools import chain
from math import log
from numpy import exp2
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from tagging.features import (History, word_lower, word_istitle, word_isupper,
                              word_isdigit, NPrevTags, PrevWord)
from tagging.features import (FollWord, word_is_first, word_is_last,
                              word_is_middle, sent_is_very_short,
                              sent_is_short)


class MEMM:

    def __init__(self, n, tagged_sents, classifier=LogisticRegression(),
                 ef=False):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        ef -- boolean specifying if extra features might be used.
        classifier -- classifier for the model.
        """
        self.n = n
        self.all_words = set(it[0] for sent in tagged_sents for it in sent)

        basic_feat = [word_lower, word_istitle, word_isupper, word_isdigit]
        features = basic_feat
        features += [PrevWord(feature) for feature in basic_feat]
        features += [NPrevTags(i) for i in range(1, n)]

        if (ef):
            features += [FollWord(feature) for feature in basic_feat]
            features += [word_is_first, word_is_last, word_is_middle]
            features += [sent_is_very_short, sent_is_short]

        self.pipeline = Pipeline([('vect', Vectorizer(features)),
                                  ('clf', classifier)])

        self.pipeline = self.pipeline.fit(
            X=list(self.sents_histories(tagged_sents)),
            y=list(self.sents_tags(tagged_sents))
        )

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        res = [self.sent_histories(tagg_sent) for tagg_sent in tagged_sents]
        return(chain(*res))

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        words = [word[0] for word in tagged_sent]
        tags = ('<s>',)*(n-1) + tuple([word[1] for word in tagged_sent])
        res = []
        for i in range(len(words)):
            res.append(History(words, tags[i:i+n-1], i))
        return(iter(res))

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        res = [self.sent_tags(tagged_sent) for tagged_sent in tagged_sents]
        return(chain(*res))

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        res = [word[1] for word in tagged_sent]
        return(iter(res))

    def tag(self, sent):
        """
        Tag a sentence.

        sent -- the sentence.
        """
        n = self.n
        res = []
        tags = ('<s>',)*(n-1)
        for i in range(len(sent)):
            history = History(sent, tags, i)
            act_tag = self.tag_history(history)
            res.append(act_tag)
            tags = (tags+(act_tag,))[1:]
        return(res)

    def tag_history(self, h):
        """
        Tag a history.

        h -- the history.
        """
        return(self.pipeline.predict([h])[0])

    def unknown(self, w):
        """
        Check if a word is unknown for the model.

        w -- the word.
        """
        return(w not in self.all_words)


class ViterbiMEMM(MEMM):

    def __init__(self, n, tagged_sents, k, classifier=LogisticRegression(),
                 ef=False):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        ef -- boolean specifying if extra features might be used.
        classifier -- classifier for the model.
        k -- save k most probable taggings.
        """
        super(ViterbiMEMM, self).__init__(n, tagged_sents, classifier, ef)
        assert (k > 0)
        self.k = k

    def tag_history_probs(self, h):
        """
        Get a history taggings probabilities.

        h -- the history.history = History(sent, tags, i)
        """
        try:
            probs = self.pipeline.predict_proba([h])[0]
        except AttributeError:
            probs = exp2(self.pipeline.decision_function([h])[0])

        indexes = sorted(range(len(probs)), key=lambda x: -probs[x])
        tags = self.pipeline.classes_[indexes]
        probs = probs[indexes]
        return(list(zip(probs, tags)))

    def tag(self, sent):
        """
        Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        self._pi = pi = defaultdict(lambda: defaultdict(tuple))
        n = self.n
        save_probs = self.k  # this name, because I use k in viterbi algorithm
        pi[0][('<s>',)*(n-1)] = (0, [])  # log prob

        for k in range(len(sent)):
            pi_k_1 = pi[k]
            pi_k = pi[k+1]
            for prev_tags in pi_k_1.keys():  # fixed w u
                history = History(sent, prev_tags, k)
                tag_probs = self.tag_history_probs(history)
                for act_prob, v in tag_probs:  # using same names as in hmm
                    act_prob = log(act_prob, 2) + pi_k_1[prev_tags][0]
                    act_tags = pi_k_1[prev_tags][1] + [v]
                    old_prob = pi_k.get((prev_tags + (v,))[1:],
                                        (float('-inf'),))[0]
                    if (old_prob < act_prob):
                        pi_k[(prev_tags + (v,))[1:]] = (act_prob, act_tags)
            # keep the k most probable from pi_k
            aux = list(pi_k.items())
            aux.sort(key=lambda x: -x[1][0])
            aux = aux[:save_probs]
            pi[k+1] = dict(aux)

        last_state = list(pi[max(pi.keys())].values())
        probs = [keys[0] for keys in last_state]
        self._pi = dict(pi)
        return last_state[probs.index(max(probs))][1]
