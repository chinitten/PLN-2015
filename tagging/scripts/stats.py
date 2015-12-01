"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict, Counter

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())
    count = 0
    # compute the statistics
    tagworddict = defaultdict(lambda: defaultdict(int))
    wordtagdict = defaultdict(lambda: (0, set()))
    lengthdict = defaultdict(list)
    taglenlist = list()
    wordcountlist = list()

    print('sents: {}'.format(len(sents)))
    for sent in sents:
        count += len(sent)
        for word in sent:
            tagworddict[word[1]][word[0]] += 1
            wordtagdict[word[0]] = (wordtagdict[word[0]][0]+1, wordtagdict[word[0]][1].union(set([word[1]])))
    print('words:', count)
    print('vocabulary:', len(wordtagdict))
    print('tags:', len(tagworddict))

    # compute advanced statistics

    for item in tagworddict.items():
        taglenlist.append((item[0], sum(item[1].values())))
    taglenlist = sorted(taglenlist, key=lambda tags: tags[1], reverse=True)
    taglenlist = taglenlist[:10]

    print("tag\tfrequency\t%\tmost5\n")
    for tag in taglenlist:
        wordcountlist = sorted(tagworddict[tag[0]].items(), key=lambda tags: tags[1], reverse=True)
        if len(wordcountlist) >= 5:
            wordcountlist = wordcountlist[:5]
        word, tags = zip(*wordcountlist)
        print("{0}\t{1}\t{2:.2%}\t{3}\n".format(tag[0], tag[1], tag[1]/count, str(word)))

    for word in wordtagdict.keys():
        lengthdict[len(wordtagdict[word][1])] += wordtagdict[word][0]*[word]
    print("n\twords\t%\texamples\n")
    for key in lengthdict.keys():
        lengthdict[key] = Counter(lengthdict[key])
        print("{0}\t{1}\t{2:.2%}\t{3}\n".format(key, len(lengthdict[key].keys()), len(lengthdict[key].keys())/len(wordtagdict), lengthdict[key].most_common(5)))
