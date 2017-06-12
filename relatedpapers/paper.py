import nltk.data

class Paper:

    def __init__(self, id, title, date, abstract, body):
        """
        A paper.
        id -- Papers id.
        title -- Papers title.
        abstract -- Papers abstract.
        body -- Papers body.
        """
        self.id = id
        self.title = title
        year = [year for year in date.split(' ') if len(year) == 4]
        self.year = None
        if (len(year) > 0):
            self.year = int(year[0])
        self.abstract = self.__split_sents(abstract)
        self.body = self.__split_sents(body)

    def get_full_paper(self):
        """
        Returns the title, abstract and body.
        """
        res = [self.title]+self.abstract+self.body
        return res

    def __split_sents(self, text):
        sents = text.split('\n')
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = tokenizer.tokenize_sents(sents)
        sents = [sent.strip() for subsents in sents for sent in subsents]
        return sents
