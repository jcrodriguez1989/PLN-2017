from featureforge.vectorizer import Vectorizer
from itertools import chain
from sklearn.pipeline import Pipeline

from tagging.features import *

class MEMM:

    def __init__(self, n, tagged_sents, classifier, ef=False):
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
        features += [NPrevTags(i) for i in range(1,n)]
        
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
        res = [self.sent_histories(tagged_sent) for tagged_sent in tagged_sents]
        return(chain(*res))

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        words = [ word[0] for word in tagged_sent ]
        tags = ('<s>',)*(n-1) + tuple([ word[1] for word in tagged_sent ])
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
        res = [ word[1] for word in tagged_sent ]
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
        return(not w in self.all_words)
