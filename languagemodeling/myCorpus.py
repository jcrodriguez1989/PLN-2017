from math import ceil
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
from random import shuffle


class MyCorpus(object):
    def __init__(self, fileName, path=".", trainPerc=1):
        """
        path -- path of the corpus file.
        fileName -- name of the corpus file.
        trainPerc -- percentage [0,1] of sentences as train data, the rest is
        test data.
        """

        assert (0 <= trainPerc) & (trainPerc <= 1)

        # load the data
        pattern = r'''(?ix)       # set flag to allow verbose regexps
            (?:sr\.|sra\.)
            | Fig\.               # figures at papers
            | GO:[0-9]*           # gene ontology ids
            | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
            | \w+(?:-\w+)*        # words with optional internal hyphens
            | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
            | \.\.\.              # ellipsis
            | [][.,;"'?():-_`]    # these are separate tokens; includes ], [
            '''
        tokenizer = RegexpTokenizer(pattern)
        corpus = PlaintextCorpusReader(path, fileName,
                                       word_tokenizer=tokenizer)

        self.sents = sents = corpus.sents()
        self.trainIdx = []
        self.testIdx = []
        self.trainSents = []
        self.testSents = []

        # esto consume tiempo, asi que lo hago solo si hay test data
        if (trainPerc < 1):
            sentsIdx = list(range(len(sents)))
            # mezclamos los indices para que train y test sean aleatorios
            shuffle(sentsIdx)
            self.trainIdx = sentsIdx[:ceil(len(sents)*trainPerc)]
            self.testIdx = sentsIdx[ceil(len(sents)*trainPerc):]

    def get_sents(self):
        """
        Corpus sentences.
        """
        return self.sents

    def get_train_sents(self):
        """
        training sentences, trainPerc must be < 1.
        """
        assert (self.trainIdx != []) | (self.testIdx != [])
        if (self.trainSents == []):
            self.trainSents = [self.sents[i] for i in self.trainIdx]
        return self.trainSents

    def get_test_sents(self):
        """
        test sentences, trainPerc must be < 1.
        """
        assert (self.trainIdx != []) | (self.testIdx != [])
        if (self.testSents == []):
            self.testSents = [self.sents[i] for i in self.testIdx]
        return self.testSents
