"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] [-c <classif>] [-e <bool>] [-k <n>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  mlhmm: Maximum Likelihood Hidde Markov Model
                  memm: Maximum Entropy Markov Model
                  viterbimemm: MEMM with viterbi tagger
  -n <n>        Order of the model (for mlhmm, memm and viterbimemm).
  -c <classif>  Classifier to use in the model (for memm and viterbimemm):
                  lr: LogisticRegression
                  mnb: MultinomialNB
                  lsvc: LinearSVC
  -e <bool>     Use extra features (memm and viterbimemm).
  -k <n>        Parameter for beam, save k most probable tagging (viterbimemm).
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
from tagging.memm import MEMM, ViterbiMEMM


models = {
    'base': BaselineTagger,
    'mlhmm': MLHMM,
    'memm': MEMM,
    'viterbimemm': ViterbiMEMM
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
    k = opts['-k']

    ef = False
    if (e != ""):
        ef = True

    if (k is not None):
        k = int(k)

    if m == 'mlhmm':
        print('MLHMM model')
        model = models[m](n, sents)
    elif m == 'memm':
        print('MEMM model')
        model = models[m](n, sents, classifiers[c], ef)
    elif m == 'viterbimemm':
        print('Viterbi MEMM model')
        print('K:', k)
        model = models[m](n, sents, k, classifiers[c], ef)
    else:
        print('baseline tagger model')
        model = models[m](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
