"""
Get the most probable reordering of sentences given an n-gram model.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
from docopt import docopt
from nltk.metrics import distance
from nltk.translate.bleu_score import sentence_bleu
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

    n = model.n
    distances = []
    bleus = []
    for sent in sents:
        actReordering = model.viterbi(sent)
        if (actReordering == []) | (actReordering is None):
            continue
        # remove trailing <s> and </s>
        actReordering = actReordering[(n-1):(-1)]
        actReorderingJoin = ''.join(actReordering)
        actSentJoin = ''.join(sent)
        assert len(actSentJoin) == len(actReorderingJoin)
        actDist = distance.edit_distance(actReorderingJoin, actSentJoin)
        distances.append(actDist / len(actSentJoin))
        # and now bleus
        actbleu = sentence_bleu([sent], actReordering)
        bleus.append(actbleu)

    print("Distancia media:", sum(distances)/len(distances))
    print("Distancia bleu media:", sum(bleus)/len(bleus))
