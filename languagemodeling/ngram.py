# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log2, ceil
from random import random


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
        assert len(prev_tokens) == n - 1

        if self.counts[tuple(prev_tokens)] == 0:
            return 0.
        else:
            return float(self.counts[tuple(prev_tokens + [token])]) / self.counts[tuple(prev_tokens)]

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        n = self.n
        result = 1
        sent = (n-1)*['<s>'] + sent
        sent.append('</s>')

        for word in range(n-1, len(sent)):
            result *= self.cond_prob(sent[word], sent[word-(n-1):word])
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

        for word in range(n-1, len(sent)):
            aux = self.cond_prob(sent[word], sent[word-(n-1):word])
            if aux == 0:
                result = float('-inf')
                break
            result += log2(aux)

        return result


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = n = model.n
        self.probs = probs = defaultdict(dict)
        if n == 1:
            for key in model.counts.keys():
                if len(key) == n:
                    probs[key[n:]].update({key[n-1]: model.cond_prob(key[n-1], list(key[n:]))})
        else:
            for key in model.counts.keys():
                if len(key) == n:
                    probs[key[:n-1]].update({key[n-1]: model.cond_prob(key[n-1], list(key[:n-1]))})

        self.sorted_probs = sorted_probs = defaultdict(dict)
        for item in probs.items():
            sorted_probs[item[0]] = sorted(item[1].items(), key=lambda x: (x[1], x[0]), reverse=False)


    def generate_sent(self):
        """Randomly generate a sentence."""

        n = self.n
        sentence = list()
        prev_tokens = list()
        prev_tokens = (n - 1) * ['<s>']
        token = self.generate_token(prev_tokens)

        while(True):
            if not token == '</s>':
                prev_tokens.append(token)
                sentence.append(token)
                prev_tokens = prev_tokens[1:]
                token = self.generate_token(prev_tokens)

            else:
                prev_tokens.append(token)
                prev_tokens = prev_tokens[1:]
                break

        return sentence



    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            prev_tokens = []
        sorted_probs = self.sorted_probs
        rand = random()
        closest = 1
        candidate = '</s>'
        for prob in sorted_probs[tuple(prev_tokens)]:
            aux = abs(rand - prob[1])
            if aux < closest:
                closest = aux
                candidate = prob[0]
            elif aux == closest:
                if random() > 0.5:
                    candidate = prob[0]

        return candidate

class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        super(AddOneNGram, self).__init__(n, sents)
        d = set()
        for sent in sents:
            sent = (n-1)*['<s>'] + sent
            sent.append('</s>')
            aux = set(sent)
            d = d.union(aux)

        if n == 1:
            self.v = len(d)
        else:
            self.v = len(d)-1

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

        if not prev_tokens:
            prev_tokens = []

        tokens = prev_tokens + [token]

        return float(self.count(tokens)+1)/(self.count(prev_tokens) + self.v)

    def V(self):
        """Size of the vocabulary.
        """
        return self.v


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        super(InterpolatedNGram, self).__init__(n, sents)

        if not gamma:
            held_out = sents[-ceil(0.1*len(sents)):]  # Take the last 10%
            sents = sents[:int(0.9*len(sents))]  # Take the first 90%

        self.gamma = gamma
        self.models = models = list()
        if addone:
            for i in range(0, n):
                models.append(AddOneNGram(i+1, sents))
        else:
            for i in range(0, n):
                models.append(NGram(i+1, sents))

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        models = self.models
        gamma = self.gamma
        if not prev_tokens:
            prev_tokens = []
        lambdas = list()
        aux = 0.
        prob = 0.
        for i in range(0, n-1):
            lambdas.append((1 - aux) * models[n - (i + 1)].count(prev_tokens) / (models[n - (i + 1)].count(prev_tokens) + gamma))
            prob += lambdas[i] * models[n - (i + 1)].cond_prob(token, prev_tokens)
            aux = sum(lambdas)
            prev_tokens = prev_tokens[1:]
        lambdas.append(1-aux)
        prob += lambdas[n-1]*models[0].cond_prob(token, prev_tokens)

        return prob

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        models = self.models
        index = len(tokens)
        if index == 0:
            index = 1

        return models[index-1].count(tokens)
