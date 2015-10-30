"""Evaulate a parser.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans , unlabelled_spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    parsed_sents = list(corpus.parsed_sents())

    print('Parsing...')
    hits, total_gold, total_model = 0, 0, 0
    unlabelled_hits, total_unlabelled_gold, total_unlabelled_model = 0, 0, 0
    n = len(parsed_sents)
    format_str = '{:3.1f}% ({}/{}) (P={:2.2f}%, R={:2.2f}%, F1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0))
    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()

        # parse
        model_parsed_sent = model.parse(tagged_sent)

        # compute labeled scores
        gold_spans = spans(gold_parsed_sent, unary=False)
        gold_unlabelled_spans = unlabelled_spans(gold_parsed_sent, unary=False)

        model_spans = spans(model_parsed_sent, unary=False)
        model_unlabelled_spans = unlabelled_spans(model_parsed_sent, unary=False)

        hits += len(gold_spans & model_spans)
        unlabelled_hits += len(gold_unlabelled_spans & model_unlabelled_spans)

        total_gold += len(gold_spans)
        total_unlabelled_gold += len(gold_unlabelled_spans)

        total_model += len(model_spans)
        total_unlabelled_model += len(model_unlabelled_spans)

        # compute labeled partial results
        prec = float(hits) / total_model * 100
        rec = float(hits) / total_gold * 100
        f1 = 2 * prec * rec / (prec + rec)

        # compute unlabelled partial results

        u_prec = float(unlabelled_hits) / total_unlabelled_model * 100
        u_rec = float(unlabelled_hits) / total_unlabelled_gold * 100
        u_f1 = 2 * u_prec * u_rec / (u_prec + u_rec)

        progress(format_str.format(float(i+1) * 100 / n, i+1, n, prec, rec, f1))

    print('')
    print('Parsed {} sentences'.format(n))
    print('Labeled')
    print('  Precision: {:2.2f}% '.format(prec))
    print('  Recall: {:2.2f}% '.format(rec))
    print('  F1: {:2.2f}% '.format(f1))
    print('Unlabelled')
    print('  Precision: {:2.2f}% '.format(u_prec))
    print('  Recall: {:2.2f}% '.format(u_rec))
    print('  F1: {:2.2f}% '.format(u_f1))
