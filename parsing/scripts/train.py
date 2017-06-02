"""Train a parser.

Usage:
  train.py [-m <model>] [-n <n>] [-u <b>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: flat]:
                  flat: Flat trees
                  rbranch: Right branching trees
                  lbranch: Left branching trees
                  upcfg: Unlexicalized PCFG.
  -n <n>        Order of horizontal Markovization for UPCFG [default: None].
  -u <b>        Admit unnary productions for UPCFG [default: False].
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.baselines import Flat, RBranch, LBranch
from parsing.upcfg import UPCFG

models = {
    'flat': Flat,
    'rbranch': RBranch,
    'lbranch': LBranch,
    'upcfg': UPCFG,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-3.0.1es/', files)

    print('Training model...')
    m = opts['-m']
    if m == 'upcfg':
        n = opts['-n']
        if n == "None":
            n = None
        else:
            n = int(n)
        u = opts['-u']
        model = models[m](corpus.parsed_sents(), horzMarkov=n, unary=u=='True')
    else:
        model = models[m](corpus.parsed_sents())

    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
