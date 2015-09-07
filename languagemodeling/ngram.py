# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log2

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            sent = (n-1)*['<s>'] + sent
            sent.append('</s>')
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tuple(tokens)]

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        #print(len(prev_tokens))
        #print(n)
        assert len(prev_tokens) == n - 1

        return float(self.counts[tuple(prev_tokens + [token])]) / self.counts[tuple(prev_tokens)]


    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        n = self.n
        result = 1
        sent = (n-1)*['<s>'] + sent
        sent.append('</s>')

        for word in range(n-1,len(sent)):
            result *= self.cond_prob(sent[word],sent[word-(n-1):word])
            if result == 0:
                break

        return result

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        n = self.n
        result = 0
        sent = (n-1)*['<s>'] + sent
        sent.append('</s>')

        for word in range(n-1,len(sent)):
            aux = self.cond_prob(sent[word],sent[word-(n-1):word])
            if aux == 0:
                result = float('-inf')
                break
            result += log2(aux)

        return result
