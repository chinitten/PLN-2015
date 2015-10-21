from math import log2

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
        """Returns the set of tags.
        """
        return self.tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        result = self.trans.get(prev_tags, 0.)
        if result is not 0.:
            result = result.get(tag,0.)

        return result

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        result = self.out.get(tag,0.)
        if result is not 0.:
            result = result.get(word,0.)

        return result

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        y -- tagging.
        """

        result = 1.
        n = self.n
        y = (n-1)*['<s>'] + y + ['</s>']
        upto = len(y)
        for i in range(n-1,upto):
            result *= self.trans_prob(y[i],tuple(y[i-n+1:i]))

        return result

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        result = 1.
        sent_tag = zip(x,y)
        for item in sent_tag:
            result *= self.out_prob(item[0],item[1])
        return result

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        result = 0.
        n = self.n
        y = (n-1)*['<s>'] + y + ['</s>']
        upto = len(y)
        for i in range(n-1,upto):
            result += log2(self.trans_prob(y[i],tuple(y[i-n+1:i])))

        return result


    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
    """
        result = 0.
        sent_tag = zip(x,y)
        for item in sent_tag:
            result += log2(self.out_prob(item[0],item[1]))
        return result

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        tagger = ViterbiTagger(self)
        return tagger.tag(sent)

class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
