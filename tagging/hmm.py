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
        self._tagset = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self._tagset

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
        return result * self.tag_prob(y)

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
        return result + self.tag_log_prob(y)

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
        m = len(sent)
        hmm = self.hmm
        n = self.hmm.n
        tagset = self.hmm.tagset()
        self._pi = pi = {}
        pi[0] = {('<s>',) * (n - 1): (0., [])}

        for k , wordtag in zip(range(1, m+1),sent):
            pi[k] = {}
            for tag_ant ,(pi_ant, list_tags) in pi[k-1].items():
                for v in tagset:
                    q = hmm.trans_prob(v,tag_ant)
                    e = hmm.out_prob(sent[k-1],v)
                    if (e!=0. and q!=0.):
                        new_prev = (tag_ant + (v,))[1:]
                        pi_new = pi_ant + log2(q) + log2(e)
                        if new_prev not in pi[k] or pi[k][new_prev] < pi_new:
                            pi[k][new_prev] = (pi_new, list_tags + [v])

        max_pi = float('-inf')
        result = None
        for tag_ant, (pi_ant, list_tags) in pi[m].items():
            q = hmm.trans_prob('</s>', tag_ant)
            if q > 0.:
                new_pi = pi_ant + log2(q)
                if new_pi > max_pi:
                    max_pi = new_pi
                    result = list_tags

        return result


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """

    def tcount(self, tokens):
        """Count for an n-gram or (n-1)-gram of tags.

        tokens -- the n-gram or (n-1)-gram tuple of tags.
        """

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        """ si es desconocida devolver 1/v

        cantidad de veces palabra x con el tag s sobre count(tag s)

        """

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        """checkeak si es addone  devolves con esmoothing sumandole el 1 / v

        count(todo) / count(prev_tags)

        """
