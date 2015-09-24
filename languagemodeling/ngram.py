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

    def log_prob(self, sents):
        """
        Log probability calculation.
        """
        result = 0.
        for sent in sents:
            aux = self.sent_log_prob(sent)
            if aux == -float('inf'):
                return aux
            result += aux
        return result

    def cross_entropy(self, sents):
        """
        Cross entropy calculation
        """
        m = 0.
        log_prob = self.log_prob(sents)
        if log_prob == -float('inf'):
            return log_prob
        for sent in sents:
            m += len(sent)
        return log_prob/m

    def perplexity(self, sents):
        """
        Perplexity calculation
        """
        cross = self.cross_entropy(sents)
        return pow(2, -cross)

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

        if gamma is None:
            held_out = sents[-ceil(0.1*len(sents)):]  # Take the last 10%
            sents = sents[:int(0.9*len(sents))]  # Take the first 90%
            self.estimate_gamma(n, sents, held_out, addone)
        else:
            self.gamma = gamma

        self.models = models = list()
        if addone:
            models.append(AddOneNGram(1, sents))
        else:
            models.append(NGram(1, sents))
        for i in range(1, n):
            models.append(NGram(i+1, sents))

    def estimate_gamma(self, n, sents, held_out, addone):
        """
        Estimates gamma with minimun perplexity from a determined range
        """
        print("Entering estimate_gamma")
        gammas = [i*10 for i in range(1, 11)]
        print(gammas)
        aux = 0.
        aux_ngram = None
        candidates = list()
        for gamma in gammas:
            aux_ngram = InterpolatedNGram(n, sents, gamma, addone)
            aux = aux_ngram.perplexity(held_out)
            candidates.append((aux, gamma))
        print(candidates)
        self.gamma = min(candidates)[1]
    #    print(self.gamma)

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


class BackOffNGram(NGram):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.

        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.addone = addone
        self.beta = beta
        self.counts = counts = list()
        self.betacounts = betacounts = list()
        self.alphadict = defaultdict(float)
        self.denomdict = defaultdict(float)
        self.Adict = defaultdict(set)
        self.n = n

        if beta is None:
            sents = sents[:int(0.9*len(sents))]  # Take the first 90%
            held_out = sents[-ceil(0.1*len(sents)):]  # Take the last 10%

        if addone:
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

        for j in range(0, n+1):
            counts.append(defaultdict(int))
            betacounts.append(defaultdict(float))

        for sent in sents:
            sent = (n-1)*['<s>'] + sent
            sent.append('</s>')
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                for j in range(0, n+1):
                    counts[j][ngram[j:]] += 1

        for j in range(1, n):
            start = ('<s>',)*j
            counts[n-j][start] = (n-j)*len(sents)

        if beta is None:
            self.estimate_beta(n, held_out)
            beta = self.beta
            for j in range(0, n+1):
                for key, value in counts[j].items():
                    self.betacounts[j][key] = value - beta
        else:
            for j in range(0, n+1):
                for key, value in counts[j].items():
                    self.betacounts[j][key] = value - beta

        self.create_A()
        self.create_alphadict()
        self.create_denomdict()

    def estimate_beta(self, n, held_out):
        """
        Estimates beta with minimun perplexity from a determined range
        """
        candidates = list()
        counts = self.counts
        self.betacounts = list()
        for beta in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            # Por cada beta se calcula un betacount.
            for j in range(0, n+1):
                self.betacounts.append(defaultdict(float))
                for key, value in counts[j].items():
                    self.betacounts[j][key] = value - beta
            self.beta = beta
            # Por cada beta,betacount se calculan alphas, denoms y As.
            self.create_A()
            self.create_alphadict()
            self.create_denomdict()

            # Valiendose de lo calculado anteriormente se calcula perplexity.
            perplexity = self.perplexity(held_out)
            candidates.append((perplexity, beta))

            # Limpio para la próxima iteración.
            self.beta = None
            self.Adict = defaultdict(set)
            self.alphadict = defaultdict(float)
            self.denomdict = defaultdict(float)
            self.betacounts = list()

        # Restauro el betacounts al valor inicial
        for j in range(0, n+1):
            self.betacounts.append(defaultdict(float))

        self.beta = min(candidates)[1]

    def create_alphadict(self):
        """
        Creates alpha dictionary
        """
        alphadict = self.alphadict
        counts = self.counts
        beta = self.beta
        n = self.n
        for j in range(0, n+1):
            for key in counts[j].keys():
                alphadict[key] = beta*len(self.A(key))/self.counts[j][key]

    def create_denomdict(self):
        """
        Creates denom dictionary
        """
        addone = self.addone
        counts = self.counts
        denomdict = self.denomdict
        n = self.n

        if addone:
            v = self.v
            for key in counts[n-1].keys():
                    denomdict[key] = 1.0 - sum((counts[n-1][(w,)]+1.0)/(counts[n][()]+v) for w in self.A(key))
        else:
            for key in counts[n-1].keys():
                    denomdict[key] = 1.0 - sum(counts[n-1][(w,)]/counts[n][()] for w in self.A(key))

        for index in range(1, n):
            for key in counts[n - (index+1)].keys():
                    denomdict[key] = 1.0 - sum(self.cond_prob(w, list(key[1:])) for w in self.A(key))

    def create_A(self):
        """
        Creates A dictionary
        """
        n = self.n
        for j in range(0, n+1):
            for key, value in self.counts[j].items():
                if (value > 0):
                    try: self.Adict[key[:-1]].add(key[-1:][0])
                    except IndexError:
                        continue

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        index = len(tokens)
        n = self.n
        return self.counts[n-index][tuple(tokens)]

    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        return self.Adict.get(tokens, set())

    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """

        return self.alphadict.get(tokens, 1.0)

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        return self.denomdict.get(tokens, 1.0)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        counts = self.counts
        betacounts = self.betacounts
        addone = self.addone

        if not prev_tokens:
            prev_tokens = []
        tokens = tuple(prev_tokens + [token])
        index = len(tokens)

        if len(prev_tokens) == 0:
            if addone:
                v = self.v
                result = float(counts[n-1][tuple([token])]+1.0) / (counts[n][()] + v)
            else:
                result = float(counts[n-1][tuple([token])]) / counts[n][()]
        else:
            if counts[n-index][tokens] > 0:
                result = float(betacounts[n-index][tokens]) / float(counts[n-index+1][tuple(prev_tokens)])
            else:
                if self.alpha(tuple(prev_tokens)) == 0:
                    result = 0.
                else:
                    result = self.alpha(tuple(prev_tokens)) * (self.cond_prob(token, prev_tokens[1:]) / self.denom(tuple(prev_tokens)))

        return result
