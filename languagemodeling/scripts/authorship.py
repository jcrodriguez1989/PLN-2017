"""
Train an n-gram model.

Usage:
  #authorship.py -n <n> [-m <model>] -o <file>
  #authorship.py -h | --help

Options:
  #-n <n>        Order of the model.
  #-m <model>    Model to use [default: ngram]:
                  #ngram: Unsmoothed n-grams.
                  #addone: N-grams with add-one smoothing.
                  #interpolated: N-grams with interpolated smoothing.
                  #backoff: N-grams with backoff smoothing.
  #-o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.ngram import AddOneNGram, NGram
from nltk.corpus import gutenberg

if __name__ == '__main__':
    opts = docopt(__doc__)

    files = gutenberg.fileids()
    shakesSents = [ gutenberg.sents(file)
                   for file in files if file.startswith("shakespeare") ]
    shakesSents = [ item for sublist in shakesSents for item in sublist ]

    chesterSents = [ gutenberg.sents(file)
                   for file in files if file.startswith("chesterton") ]
    chesterSents = [ item for sublist in chesterSents for item in sublist ]

    shakestrain = shakesSents[:int(90*len(shakesSents)/100)]
    shakesUnk = shakesSents[int(90*len(shakesSents)/100):]
    chestertrain = chesterSents[:int(90*len(chesterSents)/100)]
    chesterUnk = chesterSents[int(90*len(chesterSents)/100):]

    shakesModel = AddOneNGram(1, shakestrain)
    chesterModel = AddOneNGram(1, chestertrain)

    # multiplying together the the probabilities of all the unigrams that only
    # occur once in the 'unknown' text
    shakesUnkCounts = NGram(1, shakesUnk).counts
    chesterUnkCounts = NGram(1, chesterUnk).counts

    shakesUnkOnce = [k for k in shakesUnkCounts.keys() if 
                     shakesUnkCounts[k] == 1]
    chesterUnkOnce = [k for k in chesterUnkCounts.keys() if 
                     chesterUnkCounts[k] == 1]

    probShakesIsChester = 1
    probShakesIsShakes = 1
    for onceWord in shakesUnkOnce[:100]:
        probShakesIsShakes *= shakesModel.cond_prob(onceWord)
        probShakesIsChester *= chesterModel.cond_prob(onceWord)
        print(probShakesIsShakes)

    probShakesIsChester = 0
    probShakesIsShakes = 0
    for onceWord in shakesUnkOnce[:100]:
        probShakesIsShakes += shakesModel.sent_log_prob(list(onceWord))
        probShakesIsChester *= chesterModel.sent_log_prob(list(onceWord))
        print(probShakesIsChester)


probShakesIsShakes
probShakesIsChester


