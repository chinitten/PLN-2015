from collections import defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        self.tagworddict = tagworddict = defaultdict(lambda: defaultdict(int))
        tagcountdict = defaultdict(int)
        for sent in tagged_sents:
            for word, tag in sent:
                tagworddict[word][tag] += 1
                tagcountdict[tag] += 1
        self.most_freq_tag = max(tagcountdict.items(), key=lambda x: x[1])[0]
        self.tagworddict = dict(tagworddict)

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        if self.unknown(w):
            return self.most_freq_tag
        return max(self.tagworddict[w].items(), key=lambda x: x[1])[0]

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        value = self.tagworddict.get(w, True)
        if value is not True:
            return False
        return True
