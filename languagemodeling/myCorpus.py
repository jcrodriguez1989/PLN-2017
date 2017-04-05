from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer

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
            | GO:[0-9]*           # gene ontology ids
            | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
            | \w+(?:-\w+)*        # words with optional internal hyphens
            | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
            | \.\.\.              # ellipsis
            | [][.,;"'?():-_`]    # these are separate tokens; includes ], [
            '''
        tokenizer = RegexpTokenizer(pattern)
        corpus = PlaintextCorpusReader(path, fileName, word_tokenizer=tokenizer)
        self.sents = corpus.sents()

    def get_sents(self):
        """
        Corpus sentences
        """
        return self.sents

