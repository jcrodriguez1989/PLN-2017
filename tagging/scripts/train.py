"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] [-c <classif>] [-e <bool>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  mlhmm: Maximum Likelihood Hidde Markov Model
                  memm: Maximum Entropy Markov Model
  -n <n>        Order of the model (for mlhmm and memm).
  -c <classif>  Classifier to use in the model (for memm).
  -e <bool>     Use extra features.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

# classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM
from tagging.memm import MEMM


models = {
    'base': BaselineTagger,
    'mlhmm': MLHMM,
    'memm': MEMM
}

classifiers = {
    'lr': LogisticRegression(),
    'mnb': MultinomialNB(),
    'lsvc': LinearSVC()
}

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-3.0.1es/', files)
    sents = list(corpus.tagged_sents())

    # train the model
    n = int(opts['-n'])
    m = opts['-m']
    c = opts['-c']
    e = opts['-e']

    ef = False
    if (e != ""):
        ef = True

    if m == 'mlhmm':
        print('MLHMM model')
        model = models[m](n, sents)
    elif m == 'memm':
        print('MEMM model', c)
        model = models[m](n, sents, classifiers[c], ef)
    else:
        print('baseline tagger model')
        model = models[m](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
