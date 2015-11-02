from nltk.tree import Tree

class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.grammar = grammar

        self.nonterminals = nonterminals = []
        self.terminals = terminals = []
        self.start = grammar.start()

        productions = self.grammar.productions()

        for g in productions:
            if len(g.rhs())> 1:
                nonterminals += [g]
            elif len(g.rhs()) == 1:
                terminals += [g]
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
                for nt in nonterminals:
                    for s in range(i,j):
                        if pi[(i,s)].get(nt.rhs()[0].symbol(), None) is not None:
                            if pi[(s+1,j)].get(nt.rhs()[1].symbol(), None) is not None:
                                npi = pi[(i,s)][nt.rhs()[0].symbol()] + pi[(s+1,j)][nt.rhs()[1].symbol()] + nt.logprob()
                                if pi[(i,j)].get(nt.lhs().symbol(), None) is None or npi > pi[(i,j)][nt.lhs().symbol()]:
                                            pi[(i,j)][nt.lhs().symbol()] = npi
                                            bp[(i,j)][nt.lhs().symbol()] = Tree(nt.lhs().symbol(), [bp[(i,s)].get(nt.rhs()[0].symbol(), None),
                                                                        bp[(s+1,j)].get(nt.rhs()[1].symbol(), None)])

        prob = pi[(1,n)].get(start, None)
        tree = bp[(1,n)].get(start, None)

        return (prob,tree)
