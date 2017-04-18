"""
Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.myCorpus import MyCorpus

if __name__ == '__main__':
    opts = docopt(__doc__)

    corpus = MyCorpus(path='./languagemodeling/scripts/',
                      fileName='myCorpusTest.txt')
    sents = corpus.get_sents()

    # load the model
    modelFile = opts['-i']
    with open(modelFile, 'rb') as inFile:
        model = pickle.load(inFile)

    print(type(model), model.n)
    print(model.perplexity(sents))
