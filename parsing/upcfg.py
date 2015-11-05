from nltk.grammar import induce_pcfg, Nonterminal
from nltk.tree import Tree
from parsing.cky_parser import CKYParser
from parsing.util import unlexicalize, lexicalize

class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence', horzMarkov=False):
        """
        parsed_sents -- list of training trees.
        """
        productions = []
        if horzMarkov is True:
            for t in parsed_sents:
                tree = t.copy(deep=True)
                tree = unlexicalize(tree)
                tree.chomsky_normal_form(horzMarkov=True)
                tree.collapse_unary(collapsePOS=True)
                productions += tree.productions()
        else:
            for t in parsed_sents:
                tree = t.copy(deep=True)
                tree = unlexicalize(tree)
                tree.chomsky_normal_form()
                tree.collapse_unary(collapsePOS=True)
                productions += tree.productions()

        start = Nonterminal(start)

        grammar = induce_pcfg(start, productions)
        self.parser = CKYParser(grammar)
        self.pp = grammar.productions()
        self.start = start

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.pp

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        words, tags = zip(*tagged_sent)
        words = list(words)
        tags = list(tags)

        prob, tree = self.parser.parse(tags)
        if tree is None:
            tree = Tree(self.start.symbol(), [Tree(tag, [word]) for word, tag in tagged_sent])
        else:
            tree = lexicalize(tree, words)
            tree.un_chomsky_normal_form()

        return tree
