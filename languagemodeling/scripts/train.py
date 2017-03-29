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

from nltk.corpus import gutenberg
# from nltk.corpus import PlaintextCorpusReader # If I want to use my own corpus

from languagemodeling.ngram import NGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    gutenbergAll = gutenberg.fileids()
    gutenbergShake = [k for k in gutenbergAll if 'shakespeare' in k]
    sents = gutenberg.sents(gutenbergShake)
    # for excersice 1 as corpus we use gutenbergs Shakespeare works
    
    # uncomment the following if I want to use my own corpus
    #corpus = PlaintextCorpusReader('./languagemodeling/scripts/', 
                                   #'myCorpus.txt')
    #sents = corpus.sents()

    # train the model
    n = int(opts['-n'])
    model = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
