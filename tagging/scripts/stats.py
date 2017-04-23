"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())

    # compute the statistics
    print('sents: {}'.format(len(sents))) # number of sentences

    word_counts = defaultdict(int)
    tag_counts = defaultdict(int)
    word_tags = defaultdict(lambda : defaultdict(int))
    tag_words = defaultdict(lambda : defaultdict(int))
    for sent in sents:
        for key,val in sent:
            val = val[:2]
            word_counts[key] += 1
            tag_counts[val] += 1
            word_tags[key][val] += 1
            tag_words[val][key] += 1

    print('tokens: {}'.format(len(word_counts))) # number of tokens
    print('words: {}'.format(sum([ word_counts[key] for key in word_counts.keys() ])))
    # number of words
    print('tags: {}'.format(len(tag_counts))) # number of tags

    tag_counts_list = list(tag_counts.items())
    tag_counts_list.sort(key=lambda x: x[1], reverse=not False)
    print('most frequent tags')
    most_freq_tags = tag_counts_list[:10]
    print([ val[0] for val in most_freq_tags ])
    print([ val[1] for val in most_freq_tags ])
    total_tags = sum([val[1] for val in tag_counts_list])
    print([ val[1]/total_tags for val in most_freq_tags ])

    for tag,_ in most_freq_tags:
        act_tag_words = list(tag_words[tag].items())
        act_tag_words.sort(key=lambda x: x[1], reverse=not False)
        print("\n", tag, ":")
        print([ val[0] for val in act_tag_words][:5])

    # ambiguety
    ambiguety = [list() for _ in range(9)]
    for word_tag in word_tags.items():
        if (len(word_tag[1]) == 0):
            continue
        act_level = ambiguety[len(word_tag[1])-1]
        act_level.append(word_tag)

    for i in range(9):
        print("ambiguety", i+1)
        act_level = ambiguety[i]
        print(len(act_level))
        print(len(act_level) / total_tags)
        act_level.sort(key=lambda x: sum(x[1].values()), reverse=not False)
        print([ val[0] for val in act_level][:5])

