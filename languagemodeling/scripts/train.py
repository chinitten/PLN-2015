"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] [--addone] [-g <g>] [-b <b>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpol: Interpolated
                  backoff: Back-Off
  --addone      Set addone for interpolated ngram [default: False]
  -g <g>        Set gamma for interpolated ngram.
  -b <b>        Set beta for Back-Off ngram.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import PlaintextCorpusReader  # gutenberg
from nltk.tokenize import RegexpTokenizer

from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram


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
    # sents = gutenberg.sents('corpus.txt')
    sents = PlaintextCorpusReader('../', 'corpus.txt', word_tokenizer=tokenizer).sents()
    sents = sents[:int(0.9*len(sents))]  # Take the first 90%

    # choose & train the model
    n = int(opts['-n'])
    m = opts['-m']
    a = opts['--addone']
    g = opts['-g']
    b = opts['-b']

    if m == 'addone':
        model = AddOneNGram(n, sents)
    elif m == 'ngram':
        model = NGram(n, sents)
    elif m == 'interpol':
        if g is not None:
            g = float(g)
        model = InterpolatedNGram(n, sents, a, g)
    elif m == 'backoff':
        if b is not None:
            b = float(b)
        model = BackOffNGram(n, sents, b, a)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
