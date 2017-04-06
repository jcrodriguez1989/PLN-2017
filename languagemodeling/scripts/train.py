"""
Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.myCorpus import MyCorpus
from languagemodeling.ngram import NGram

if __name__ == '__main__':
    opts = docopt(__doc__)

    corpus = MyCorpus(path='./languagemodeling/scripts/',
                        # fileName='myCorpusLittle.txt')  # delete "Little"
                        fileName='myCorpus.txt')
    sents = corpus.get_sents()

    # train the model
    n = int(opts['-n'])
    m = opts['-m']

    if m == "addone":
        model = AddOneNGram(n, sents)
    else:
        model = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
