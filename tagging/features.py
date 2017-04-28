from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()

def word_istitle(h):
    """Feature: current word starts with an uppercase letter.

    h -- a history.
    """
    

def word_isupper(h):
    """Feature: current word is uppercased.

    h -- a history.
    """
    

def word_isdigit(h):
    """Feature: current word is a number.

    h -- a history.
    """
    

class NPrevTags(Feature):

    def __init__(self, n):
        """Feature: n previous tags tuple.

        n -- number of previous tags to consider.
        """

    def _evaluate(self, h):
        """n previous tags tuple.

        h -- a history.
        """


class PrevWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the previous word.

        f -- the feature.
        """

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.

        h -- the history.
        """

def NPrevTags(n):
    """Feature: tuple of the last n tags.

    n -- last n tags.
    """
    

def PrevWord(f):
    """Feature: given a feature f, apply it over lat word.

    f -- a feature.
    """
    
