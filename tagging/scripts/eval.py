"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader
from collections import defaultdict

def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total, unknown, unk_hits = 0., 0., 0., 0.
    n = len(sents)
    matrix = defaultdict(lambda: defaultdict(float))
    matrixcount = defaultdict(float)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        tagmiss = zip(word_sent,gold_tag_sent,model_tag_sent)


        for word, gold_tag, tag in tagmiss:
            # check if unknown
            if model.unknown(word):
                unknown += 1.
                # when unknown check if tag hit happens
                if gold_tag == tag:
                    unk_hits += 1.
                else:
                    matrix[gold_tag][tag] += 1.
                    matrixcount[gold_tag] += 1.

        progress('Accuracy {:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))

    for tag, dic in matrix.items():
        for tg, num in matrix[tag].items():
            matrix[tag][tg] = matrix[tag][tg]/matrixcount[tag]

    acc = float(hits) / total
    unk_acc = unk_hits / unknown
    diff_acc = (float(hits) - unk_hits) / (total - unknown)

    print('')
    print("Confusion Matrix")
    print(matrix)
    print('')
    print('Unknown Accuracy: {:2.2f}%'.format(unk_acc * 100))
    print('')
    print('Known Accuracy: {:2.2f}%'.format(diff_acc * 100))
    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))
