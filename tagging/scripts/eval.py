"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()

def data_frame_to_md(data_frame):
    line = "| | "
    for i in data_frame.columns:
        line += i + " | "
    print(line)
    line = "| ---- | " + "---- | " * len(data_frame.columns)
    print(line)
    for i in data_frame.columns:
        line = "| " + i + " |"
        for j in data_frame.index:
            line += " " + str(conf_matrix[i][j]) + " |"
        print(line)

def plot_confusion_matrix(cm, classes, filename="cnf_matrix.pdf",
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plt.figure()

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    plt.savefig(filename)

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total = 0, 0
    known_hits, known_total = 0, 0
    unknown_hits, unknown_total = 0, 0
    n = len(sents)

    #model_tags = set(model.tags.values())
    #gold_tags = [ [word[1][:2] for word in sent] for sent in sents ]
    #gold_tags = set([item for sublist in gold_tags for item in sublist])
    #all_tags = model_tags | gold_tags
    #all_tags = [ _ for _ in all_tags]
    #conf_matrix = DataFrame(0, index=all_tags, columns=all_tags)

    # for confusion matrix
    y_test = []
    y_pred = []

    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)
        # we use just the two first chars of tags
        gold_tag_sent = [ tag[:2] for tag in gold_tag_sent ]

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        y_test = y_test + list(gold_tag_sent)
        y_pred = y_pred + model_tag_sent
        #for j in range(len(model_tag_sent)):
            #word_tag = model_tag_sent[j]
            #gold_tag = gold_tag_sent[j]
            #gold_tag = gold_tag[:2]
            ## first index is for column, second for row
            #conf_matrix[word_tag][gold_tag] += 1

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        # known words score
        hits_known = [ hits_sent[j] for j in range(len(hits_sent)) if
                      not model.unknown(word_sent[j])]
        known_hits += sum(hits_known)
        known_total += len(hits_known)

        # unknown words score
        hits_unknown = [ hits_sent[j] for j in range(len(hits_sent)) if
                      model.unknown(word_sent[j])]
        unknown_hits += sum(hits_unknown)
        unknown_total += len(hits_unknown)

        progress('{:3.1f}% Global score: ({:2.2f}%), Known words score: ({:2.2f}%), Unknown words score: ({:2.2f}%)'.format(
            float(i) * 100 / n, acc * 100,
            float(known_hits)/known_total * 100,
            float(unknown_hits)/unknown_total * 100))

    acc = float(hits) / total

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))

    print('Known words accuracy: {:2.2f}%'.format(
        float(known_hits)/known_total * 100))

    print('Unknown words accuracy: {:2.2f}%'.format(
        float(unknown_hits)/unknown_total * 100))

    #data_frame_to_md(conf_matrix)
    cnf_matrix = confusion_matrix(y_test, y_pred)
    classes = list(set(y_test) | set(y_pred))
    plot_confusion_matrix(cnf_matrix, classes, 
                          filename.split('.')[0]+'.pdf')


