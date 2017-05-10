from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """
    Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()

def word_istitle(h):
    """
    Feature: current word starts with an uppercase letter.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()

def word_isupper(h):
    """
    Feature: current word is uppercased.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()

def word_isdigit(h):
    """
    Feature: current word is a number.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isnumeric()

def prev_tags(h):
    """
    Feature: previous tags.

    h -- a history.
    """
    return h.prev_tags

### Additional features

def word_is_first(h):
    """
    Feature: current word is the first of the sentence.

    h -- a history.
    """
    i = h.i
    return i == 0

def word_is_last(h):
    """
    Feature: current word is the last of the sentence.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return i == len(sent)

def word_is_middle(h):
    """
    Feature: current word is not the fisrt nor last of the sentence.

    h -- a history.
    """
    return not (word_is_first(h) | word_is_last(h))

def sent_is_very_short(h):
    """
    Feature: current sentence is shorter than 3 words.

    h -- a history.
    """
    return len(h.sent) <= 3

def sent_is_short(h):
    """
    Feature: current sentence len is between 3 and 7 words.

    h -- a history.
    """
    return (3 < len(h.sent)) & (len(h.sent) <= 7)

class NPrevTags(Feature):

    def __init__(self, n):
        """
        Feature: n previous tags tuple.

        n -- number of previous tags to consider.
        """
        assert n > 0
        self.n = n

    def _evaluate(self, h):
        """
        n previous tags tuple.

        h -- a history.
        """
        n = self.n
        return prev_tags(h)[-n:]

class PrevWord(Feature):

    def __init__(self, f):
        """
        Feature: the feature f applied to the previous word.

        f -- the feature.
        """
        self.f = f

    def _evaluate(self, h):
        """
        Apply the feature to the previous word in the history.

        h -- the history.
        """
        f = self.f
        res = 'BOS'
        if (h.i != 0):
            res = f(History(h.sent, h.prev_tags, (h.i)-1))
        return str(res) # tests want result as string

class FollWord(Feature):

    def __init__(self, f):
        """
        Feature: the feature f applied to the following word.

        f -- the feature.
        """
        self.f = f

    def _evaluate(self, h):
        """
        Apply the feature to the following word in the history.

        h -- the history.
        """
        f = self.f
        res = 'EOS'
        if (h.i < len(h.sent)-1):
            res = f(History(h.sent, h.prev_tags, (h.i)+1))
        return str(res) # tests want result as string
