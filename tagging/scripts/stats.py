"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())

    # compute the statistics
    print('sents: {}'.format(len(sents))) # number of sentences

    counts = defaultdict(int)
    for sent in sents:
        for key,val in sent:
            counts[key] += 1

    print('tokens: {}'.format(len(counts))) # number of tokens
    print('words: {}'.format(sum([ counts[key] for key in counts.keys() ])))
    # number of words
