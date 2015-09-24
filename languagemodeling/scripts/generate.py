""" Generate natural language sentences using a language model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""

from docopt import docopt
import pickle

from languagemodeling.ngram import NGramGenerator

if __name__ == '__main__':
    opts = docopt(__doc__)

    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)

    n = int(opts['-n'])

    generator = NGramGenerator(model)
    sents = list()
    for i in range(0, n):
        sents.append(generator.generate_sent())
    print(sents)
