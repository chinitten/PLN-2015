from nltk.tree import Tree
from collections import defaultdict

class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.grammar = grammar

        self.nonterminals = nonterminals = defaultdict(list)
        self.terminals = terminals = []
        self.start = grammar.start()

        productions = self.grammar.productions()

        for g in productions:
            if len(g.rhs())> 1:
                y = g.rhs()[0].symbol()
                z = g.rhs()[1].symbol()
                nonterminals[(y,z)] += [(g.lhs(),g.logprob())]
            elif g.is_lexical():
                terminals += [g]
        self.nonterminals = dict(nonterminals)
        self._pi = dict()
        self._bp = dict()

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """
        n = len(sent)
        terminals = self.terminals
        nonterminals = self.nonterminals
        start = str(self.start)
        npi = 0.
        pi = self._pi
        bp = self._bp

        for i in range(1, n+1):
            pi[(i,i)] = dict()
            bp[(i,i)] = dict()
            for t in terminals:
                if t.rhs()[0] == sent[i-1]:
                    pi[(i,i)][t.lhs().symbol()] = t.logprob()
                    bp[(i,i)][t.lhs().symbol()] = Tree(t.lhs().symbol(),[t.rhs()[0]])

        for l in range(1,n+1):
            for i in range(1,n-l+1):
                j = i + l
                pi[(i,j)] = dict()
                bp[(i,j)] = dict()
                for s in range(i,j):
                    for y in pi[(i,s)].keys():
                        for z in pi[(s+1,j)].keys():
                            xs = nonterminals.get((y,z), None)
                            if xs is not None:
                                for x in xs:
                                    npi = pi[(i,s)][y] + pi[(s+1,j)][z] + x[1]
                                    if pi[(i,j)].get(x[0].symbol(), None) is None or npi > pi[(i,j)][x[0].symbol()]:
                                        pi[(i,j)][x[0].symbol()] = npi
                                        bp[(i,j)][x[0].symbol()] = Tree(x[0].symbol(), [bp[(i,s)].get(y, None), bp[(s+1,j)].get(z, None)])

        prob = pi[(1,n)].get(start, None)
        tree = bp[(1,n)].get(start, None)

        return (prob,tree)
