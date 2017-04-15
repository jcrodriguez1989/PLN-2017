"""
Train an n-gram model.

Usage:
  authorship.py -a <author1> -b <author2>
  authorship.py -h | --help

Options:
  -a <author1>        Name of author1 (as listed in gutenberg.fileids()).
  -b <author2>        Name of author2 (as listed in gutenberg.fileids()).
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.ngram import AddOneNGram, NGram
from nltk.corpus import gutenberg

if __name__ == '__main__':
    opts = docopt(__doc__)

    author1 = opts['-a']
    author2 = opts['-b']

    files = gutenberg.fileids()
    a1Sents = [ gutenberg.sents(file)
                   for file in files if file.startswith(author1) ]
    a1Sents = [ item for sublist in a1Sents for item in sublist ]

    a2Sents = [ gutenberg.sents(file)
                   for file in files if file.startswith(author2) ]
    a2Sents = [ item for sublist in a2Sents for item in sublist ]

    trainPerc = 90
    a1train = a1Sents[:int(trainPerc*len(a1Sents)/100)]
    a1Unk = a1Sents[int(trainPerc*len(a1Sents)/100):]
    a2train = a2Sents[:int(trainPerc*len(a2Sents)/100)]
    a2Unk = a2Sents[int(trainPerc*len(a2Sents)/100):]

    a1Model = AddOneNGram(1, a1train)
    a2Model = AddOneNGram(1, a2train)

    # multiplying together the the probabilities of all the unigrams that only
    # occur once in the 'unknown' text
    a1UnkCounts = NGram(1, a1Unk).counts
    a2UnkCounts = NGram(1, a2Unk).counts

    a1UnkOnce = [k for k in a1UnkCounts.keys() if a1UnkCounts[k] == 1]
    a2UnkOnce = [k for k in a2UnkCounts.keys() if a2UnkCounts[k] == 1]

    #probA1IsA2 = 1
    #probA1IsA1 = 1
    #for onceWord in a1UnkOnce:
        #probA1IsA1 *= a1Model.cond_prob(onceWord)
        #probA1IsA2 *= a2Model.cond_prob(onceWord)

    # multiplying these probabilities makes it 0, so lets try log prob
    probA1IsA2 = 0
    probA1IsA1 = 0
    for onceWord in a1UnkOnce:
        probA1IsA1 += a1Model.sent_log_prob(list(onceWord))
        probA1IsA2 += a2Model.sent_log_prob(list(onceWord))

    # taking the geometric mean of these (i.e. the wth root, where n is the 
    # number of probabilities you multiplied).
    ## nthRoot(p(s1)*...*p(sn)) == 2**(log2( nthRoot(p(s1)*...*p(sn)) )) ==
    ## 2**(log2( p(s1)*...*p(sn) ) / n) == 
    ## 2**(( log2(p(s1))+...+log2(p(sn)) ) / n)
    probA1IsA1 = 2**(probA1IsA1/len(a1UnkOnce))
    probA1IsA2 = 2**(probA1IsA2/len(a1UnkOnce))
    print(probA1IsA1, probA1IsA2, 
          probA1IsA1 > probA1IsA2)

    # And for the other text
    probA2IsA1 = 0
    probA2IsA2 = 0
    for onceWord in a2UnkOnce:
        probA2IsA1 += a1Model.sent_log_prob(list(onceWord))
        probA2IsA2 += a2Model.sent_log_prob(list(onceWord))

    probA2IsA1 = 2**(probA2IsA1/len(a2UnkOnce))
    probA2IsA2 = 2**(probA2IsA2/len(a2UnkOnce))
    print(probA2IsA1, probA2IsA2, 
          probA2IsA1 > probA2IsA2)



