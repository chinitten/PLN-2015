"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import PlaintextCorpusReader #gutenberg
from nltk.tokenize import RegexpTokenizer

from languagemodeling.ngram import NGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    pattern = r'''(?ix)    # set flag to allow verbose regexps
      (sr\.|sra\.)
    | ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*        # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
    | \.\.\.            # ellipsis
    | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''

    tokenizer = RegexpTokenizer(pattern)

    # load the data
    #sents = gutenberg.sents('corpus.txt')
    sents = PlaintextCorpusReader('../','corpus.txt', word_tokenizer=tokenizer).sents()

    print(sents[0])

    # train the model
    n = int(opts['-n'])
    model = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
