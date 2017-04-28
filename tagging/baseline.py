from collections import defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        # load the data
        word_tags = defaultdict(lambda: defaultdict(int))
        self.tags = tags = defaultdict(str)
        for sent in tagged_sents:
            for key, val in sent:
                word_tags[key][val] += 1
        for word, tag in word_tags.items():
            word_tag = list(tag.items())
            word_tag.sort(key=lambda x: x[1], reverse=not False)
            tags[word] = word_tag[0][0]

        self.unknown_tag = 'nc0s000'

    def tag(self, sent):
        """
        Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """
        Tag a word.

        w -- the word.
        """
        act_tag = self.tags[w]
        if (act_tag == ''):
            return self.unknown_tag
        return act_tag

    def unknown(self, w):
        """
        Check if a word is unknown for the model.

        w -- the word.
        """
        act_tag = self.tags[w]
        return act_tag == ''
