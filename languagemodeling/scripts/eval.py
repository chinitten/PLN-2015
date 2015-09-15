""" Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""

from docopt import docopt
import pickle
from math import ceil

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer


if __name__ == '__main__':
    opts = docopt(__doc__)

    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)

    pattern = r'''(?ix)    # set flag to allow verbose regexps
      (sr\.|sra\.)
    | ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*        # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
    | \.\.\.            # ellipsis
    | [][.,;"'?():-_`]  # these are separate tokens; includes ],
    '''

    tokenizer = RegexpTokenizer(pattern)

    sents = PlaintextCorpusReader('../', 'corpus.txt', word_tokenizer=tokenizer).sents()
    sents = sents[-ceil(0.1*len(sents)):]  # Take the last 10%

    log_prob = 0.
    m = 0
    for sent in sents:
        log_prob += model.sent_log_prob(sent)
        m += len(sent)
    l = log_prob/m
    perplexity = pow(2, -l)
    print(perplexity)
