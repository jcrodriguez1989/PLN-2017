from tagging.features import *

class MEMM:

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        self.tagged_sents = tagged_sents

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """

    def tag(self, sent):
        """
        Tag a sentence.

        sent -- the sentence.
        """

    def tag_history(self, h):
        """
        Tag a history.

        h -- the history.
        """

    def unknown(self, w):
        """
        Check if a word is unknown for the model.

        w -- the word.
        """
