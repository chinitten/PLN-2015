"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import PlaintextCorpusReader #gutenberg
from nltk.tokenize import RegexpTokenizer

from languagemodeling.ngram import NGram , AddOneNGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    pattern = r'''(?ix)    # set flag to allow verbose regexps
      (sr\.|sra\.)
    | ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*        # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
    | \.\.\.            # ellipsis
    | [][.,;"'?():-_`]  # these are separate tokens; includes ],
    '''

    tokenizer = RegexpTokenizer(pattern)

    # load the data
    #sents = gutenberg.sents('corpus.txt')
    sents = PlaintextCorpusReader('../','corpus.txt', word_tokenizer=tokenizer).sents()
    sents = sents[:int(0.9*len(sents))] #Take the first 90%

    # choose & train the model
    n = int(opts['-n'])
    m = opts['-m']
    if m == 'addone':
        model = AddOneNGram(n, sents)
    elif m == 'ngram':
        model = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
