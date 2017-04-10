"""
Evaulate a language model using the test set.

Usage:
  eval.py -i <file> -t <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -t <file>     Test data file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    modelFile = opts['-i']
    with open(modelFile, 'rb') as inFile:
        model = pickle.load(inFile)

    # load the test sents
    testFile = opts['-t']
    with open(testFile, 'rb') as inFile:
        testSents = pickle.load(inFile)

    print(model.perplexity(testSents))