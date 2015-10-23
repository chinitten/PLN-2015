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
    """Feature: is the current word titlecased?

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()

def word_isupper(h):
    """Feature: is the current word uppercased?

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()

def word_isdigit(h):
    """Feature: is the current word a digit?

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isdigit()

def prev_tags(h):
    """Feature: returns the previos tags

    h -- a history.
    """
    return str(h.prev_tags)

class NPrevTags(Feature):

    def __init__(self, n):
        """Feature: n previous tags tuple.

        n -- number of previous tags to consider.
        """
        self.n = n

    def _evaluate(self, h):
        """n previous tags tuple.

        h -- a history.
        """
        n = self.n
        prev_tags = h.prev_tags
        prev_tags = prev_tags[-n:]
        return str(prev_tags)

class PrevWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the previous word.

        f -- the feature.
        """
        self.feature = f

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.

        h -- the history.
        """
        if h.i == 0:
            return 'BOS'
        else:
            history = History(h.sent,h.prev_tags,h.i-1)
        return str(self.feature(history))
